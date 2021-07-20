import base64

import cv2
import pytesseract
from image_parser.models import TableCellFromImage, TableFromImage, TableRowFromImage


def trim_image(img):
    thresh, b = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    binary_image = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    row = binary_image.shape[0]
    column = binary_image.shape[1]
    edges_row = []
    edges_column = []
    bottom = top = left = right = -1
    for i in range(2, row):
        table_pixels = 0
        for j in range(column):
            if binary_image[i][j] == 0:
                table_pixels += 1
        if table_pixels * 100 / column > 10:
            bottom = i
            break
    for i in reversed(range(row - 2)):
        table_pixels = 0
        for j in range(column):
            if binary_image[i][j] == 0:
                table_pixels += 1
        if table_pixels * 100 / column > 10:
            top = i
            break
    for j in range(2, column):
        table_pixels = 0
        for i in range(row):
            if binary_image[i][j] == 0:
                table_pixels += 1
        if table_pixels * 100 / row > 10:
            left = j
            break
    for j in reversed(range(column - 2)):
        table_pixels = 0
        for i in range(row):
            if binary_image[i][j] == 0:
                table_pixels += 1
        if table_pixels * 100 / row > 10:
            right = j
            break
    print('bottom,top,left,right', bottom, top, left, right)
    img = img[bottom:top, left:right]
    return img


def get_table_cells(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (750, 900))
    img = trim_image(img)
    img = cv2.resize(img, (750, 900))
    # v_lines = [98, 185, 279, 335, 427, 494, 537, 623, 669, 707, 750]
    # v_lines = [92, 181, 277, 335, 427, 498, 545, 630, 676, 716, 750]
    y_lines = [0, 92, 181, 277, 335, 427, 491, 545, 630, 672, 716, 750]
    x_lines = [84,128, 150, 172, 194, 216, 238, 260, 282, 304, 326, 348, 370, 392,
               414, 436, 458, 480, 502, 524, 546, 569, 591, 613, 635, 657, 679,
               701, 723, 745, 767, 789, 811, 833, 855, 877, 899]
    # for x in v_lines:
    #     cv2.line(img, (x, 65), (x, 900), color=(0, 0, 255), thickness=1)
    # for y in range(12800, 90000, 2205):
    #     cv2.line(img, (0, int(y / 100)), (750, int(y / 100)), color=(0, 0, 255), thickness=1)
    table = TableFromImage()
    table.total_columns = len(y_lines) - 1
    table.total_rows = len(x_lines) - 1
    rows = []
    cells = []

    '''
    table.total_columns = 1
    table.total_rows = 1
    row = TableRowFromImage()
    row.table = table
    row.row = 0
    table_cell = TableCellFromImage()
    table_cell.row = row
    success, cell_img_encoded = cv2.imencode('.png', img)
    table_cell.image = base64.b64encode(cell_img_encoded.tobytes()).decode('ascii')
    table_cell.text = 'Text'
    table_cell.column = 0
    return table, [row], [table_cell]
    '''


    for i, x in enumerate(x_lines):
        row = TableRowFromImage()
        row.table = table
        row.row = i
        rows.append(row)
        for j, y in enumerate(y_lines):
            if i == len(x_lines) - 1 or j == len(y_lines) - 1:
                break
            cell_img_orig = img[x:x_lines[i + 1], y:y_lines[j + 1]]
            cell_img = cell_img_orig
            if i ==0 or (j == 0 and i % 2 == 1):
                cell_img = 255 - cell_img
                thresh, cell_img = cv2.threshold(cell_img, 50, 255, cv2.THRESH_BINARY)
            else:
                thresh, cell_img = cv2.threshold(cell_img, 120, 255, cv2.THRESH_BINARY)
            cell_img = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
            # cell_img = cv2.GaussianBlur(cell_img, (9, 9), 0)
            # cell_img = cv2.adaptiveThreshold(cell_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 30)
            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
            # border = cv2.copyMakeBorder(cell_img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255, 255])
            # resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            # dilation = cv2.dilate(resizing, kernel, iterations=1)
            # erosion = cv2.erode(dilation, kernel, iterations=1)
            # print(pytesseract.image_to_string(erosion, lang='eng', config='--psm 7 digits'))
            # print(pytesseract.image_to_string(erosion, lang='eng', config='digits'))
            # print(pytesseract.image_to_string(cell_img, lang='eng', config='--psm 7 digits'))
            # print(pytesseract.image_to_string(cell_img, lang='eng', config='--psm 13 -c tessedit_char_whitelist=ABCDEFG0123456789'))
            # cv2.imshow("Test", erosion)
            # cv2.waitKey(0)
            output_str = pytesseract.image_to_string(cell_img, lang='eng',
                                                     config='--psm 13 -c tessedit_char_whitelist=ABCDEFG0123456789')
            cell_value = ''.join(ch for ch in output_str if ch.isalnum())
            table_cell = TableCellFromImage()
            table_cell.row = row
            success, cell_img_encoded = cv2.imencode('.jpg', cell_img_orig)
            success, cell_img_processed_encoded = cv2.imencode('.jpg', cell_img)
            table_cell.image = base64.b64encode(cell_img_encoded.tobytes()).decode('ascii')
            table_cell.processed_image = base64.b64encode(cell_img_processed_encoded.tobytes()).decode('ascii')
            table_cell.text = cell_value
            table_cell.column = j
            cells.append(table_cell)
    return table, rows, cells
