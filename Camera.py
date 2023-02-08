class Camera:
    def __init__(self, width, height, zoom):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.offset_x = 0
        self.offset_y = 0
        # offset_x, offset_y, width, height
        # offset is done from top left corner of element
        # assumes element is a box
        self.current_element = [0, 0, 0, 0]
        self.zoom = zoom
        self.element_padding = 100

    def center_around_element(self, element_width, element_height):
        element_center_x = element_width // 2
        element_center_y = element_height // 2
        self.offset_x = self.center_x - element_center_x
        self.offset_y = self.center_y - element_center_y
        self.current_element = [self.offset_x, self.offset_y, element_width, element_height]

    def move_x(self, x):
        # el_offset_x, _, el_width, _ = self.current_element
        # if (el_offset_x + el_width * self.zoom + x + self.element_padding) > self.width and (el_offset_x + x - self.element_padding) < 0:
        self.offset_x += x
        self.current_element[0] += x

    def move_y(self, y):
        # _, el_offset_y, _, el_height = self.current_element
        # if (el_offset_y + el_height * self.zoom + y + self.element_padding) > self.height and (el_offset_y + y - self.element_padding) < 0:
        self.offset_y += y
        self.current_element[1] += y
