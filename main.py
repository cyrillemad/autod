import base64
import tomllib

build_path = "build.svg"
select_id = "image0_1081_1069"

with open("config.toml", "rb") as cfg:
    config = tomllib.load(cfg)

with open(config['template_svg'], "r") as svg:
    data = svg.read()


def decompose_image(data):
    first = -1
    last = -1
    result = []

    for i in range(len(data)):
        char = data[i]
        if char == "<":
            checkword = data[i + 1:i + 6]
            if checkword == "image":
                first = i + 1
        elif char == ">" and first != -1:
            last = i + 1
            result.append((data[first:last], first))
            first, last = -1, -1

    return result


def get_property(string, property):
    is_undefined = True
    edges = []

    for i in range(len(string)):
        if len(edges) == 2:
            break
        elif (string[i] == property[0] and is_undefined):
            for j in range(len(property)):
                if string[i + j] == property[j]:
                    if j + 1 == len(property):
                        is_undefined = False
                else:
                    break
        elif string[i] == '"' and not is_undefined:
            edges.append(i + 1)
    return edges


def get_data(decomposed):
    image_pack = select_image_by_id(decomposed, select_id)
    image, move = image_pack[0], image_pack[1]
    edges = get_property(image, "xlink:href")
    return decomposed[edges[0] + move:edges[1] - 1 + move]


def template_to_base64(path):
    with open(path, "rb") as image_file:
        base64_byte = base64.b64encode(image_file.read())
        return "data:image/png;base64," + str(base64_byte)[2:-1]

def select_image_by_id(pack, id):
    for element_pack in pack:
        element = element_pack[0]
        if get_property(element, id) != []:
            return element_pack

def build_svg(svg, picture):

    image_pack = select_image_by_id(decompose_image(svg), select_id)
    addon = template_to_base64(picture)
    image, move = image_pack[0], image_pack[1]
    data_edges = get_property(image, "xlink:href")
    before_image_slice = svg[0:data_edges[0] + move]
    after_image_slice = svg[data_edges[1] - 1 + move:-1]

    build = before_image_slice + addon + after_image_slice
    buildname = 'build.svg' # todo: generation of packs svg from packs input pictures
    with open(config['build_place'] + buildname, "w") as file:
        file.write(build)


build_svg(data, config['change_picture'])
