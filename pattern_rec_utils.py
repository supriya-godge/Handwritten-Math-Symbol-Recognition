"""
Utility modules for various Pattern Recognition functions

@author: Ajinkya Dhaigude (ad8454@rit.edu)
@author: Supriya Godge (spg5835@rit.edu)
"""


def scale_all_inkml(all_inkml, max_coord):
    """
    Scale and update all the coordinates in the Inkml objects.

    :param all_inkml: list of Inkml objects
    :param max_coord: maximum scaled y coordinate
    :return: None
    """

    for inkml in all_inkml:

        # list to store all strokes in this Inkml object
        all_strokes = []
        for trace_id, coords in inkml.strokes.items():
            all_strokes.append(coords)

        # get the scaled coordinates for this Inkml object
        all_scaled_strokes = get_scaled_symbol(all_strokes, max_coord)

        # update this Inkml object with scaled coordinates
        inkml.update_strokes(all_scaled_strokes)


def get_scaled_symbol(strokes, max_coord):
    """
    Scale all coordinates to a specified range.

    :param strokes: list containing all stroke coordinates for a symbol. eg: ['2 35, 45 30', '10 15, 20 12, 89 54']
    :param max_coord: maximum y coordinate in the new scale
    :return: list of zipped x and y coordinates
    """

    symbol = []
    min_x = float('infinity')
    min_y = float('infinity')
    max_x = 0
    max_y = 0
    temp = []

    for stroke in strokes:
        # fetch each data point coordinate and append to lists
        stroke = stroke.strip('\n').split(',')
        x = []
        y = []

        for point in stroke:
            point = [val for val in point.split(' ') if len(val) > 0]
            x.append(float(point[0]))
            y.append(float(point[1]))

        # compute the minimum and maximum of all x and y coordinates
        min_x = min(min(x), min_x)
        min_y = min(min(y), min_y)
        max_x = max(max(x), max_x)
        max_y = max(max(y), max_y)

        temp.append((x, y))

    # generate scaling factor
    diff_x, diff_y = max_x - min_x, max_y - min_y
    if diff_x == 0:
        diff_x = 1
    if diff_y == 0:
        diff_y = 1

    pad_y = 1
    pad_x = 1

    # scale y to max_coord and x to corresponding aspect ratio
    scale_y = (max_coord - 1) / diff_y
    new_max = max_x * max_coord / diff_y
    new_min = min_x * max_coord / diff_y
    scale_x = (new_max - new_min) / diff_x

    # apply scaling computation
    for x, y in temp:
        x = [(scale_x * (ele - min_x)) + pad_x for ele in x]
        y = [(scale_y * (ele - min_y)) + pad_y for ele in y]
        symbol.append(zip(x, y))

    return symbol


def write_to_lg(all_inkml, path=''):
    """
    Write a new .lg file in the Object format for each inkml file.

    :param all_inkml: list of Inkml objects
    :param path: path to output directory
    :return: None
    """

    for inkml in all_inkml:
        with open(path+inkml.ui+'.lg') as new_file:
            new_file.write(inkml.get_objects_str)


def print_view_symbols_html(all_inkml, max_coord):
    """
    Prints all input strokes as a normalized svg image in html

    :param all_strokes: list of Inkml objects
    :param max_coord: maximum y coordinate of symbol
    :return: None
    """

    # get list of all scaled strokes
    all_strokes = []
    for inkml in all_inkml:
        strokes = list(inkml.strokes.values())
        all_strokes.append(strokes)

    # initialize html file with header info
    html = '<html><style> svg, h2, h3, div{padding:30px;text-align:center}</style><body>\n'

    # append svg html code in a sorted manner
    for symbol in all_strokes:
        html += '<div>' + draw_svg(max_coord, symbol) + '</div>'

    html += '</div>\n </body></html>'

    # print html code to console
    print(html)


def draw_svg(max_coord, all_strokes):
    """
    Generate code to display svg image.

    :param max_coord: svg image width
    :param all_strokes: stroke coordinates
    :return: string containing html code for displaying svg image
    """

    # set the svg height and compute width as max x in loop
    ht = max_coord + 45
    width = 0
    svg_html = ''

    # add coordinates to code
    for stroke in all_strokes:
        svg_html += '\n<polyline points="'
        for x, y in stroke:
            svg_html += str(x) + ',' + str(y) + ' '
            width = max(width, x)

        svg_html += '" style="fill:none;stroke:black"/>'

    # prepend code for svg size
    svg_html = '\n<svg height="' + str(ht) + '" width="' + str(width+2) + '">' + svg_html

    return svg_html
