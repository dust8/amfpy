from io import BytesIO
from struct import unpack
from amfpy.marker import *


class AMFReader:

    def __init__(self, data):
        self.data = data
        self.bi = BytesIO(data)
        self.pos = 0

    def read(self, size):
        self.pos += size
        return self.bi.read(size)


def decode_amf_packet(reader):
    d = {}
    version = unpack('>H', reader.read(2))[0]
    header_count = unpack('>H', reader.read(2))[0]
    d['version'] = version
    d['header_count'] = header_count
    if header_count > 0:
        decode_header_type()
    message_count = unpack('>H', reader.read(2))[0]
    d['message_count'] = message_count
    d['message_type'] = decode_message_type(reader)
    return d


def decode_header_type():
    pass


def decode_message_type(reader):
    target_uri_length = unpack('>H', reader.read(2))[0]
    target_uri_string = reader.read(target_uri_length).decode()
    response_uri_length = unpack('>H', reader.read(2))[0]
    response_uri_string = reader.read(response_uri_length).decode()
    message_length = unpack('>I', reader.read(4))[0]
    value_type = read_value_type(reader)
    return {'target_uri': target_uri_string,
            'response_uri': response_uri_string,
            'message_length': message_length,
            'value_type': value_type}


def read_utf8(reader):
    length = unpack('>H', reader.read(2))[0]
    return reader.read(length).decode()


def read_utf8_long(reader):
    length = unpack('>I', reader.read(4))[0]
    return reader.read(length)


def read_number(reader):
    return unpack('>d', reader.read(8))[0]


def read_boolean(reader):
    n = unpack('>B', reader.read(1))[0]
    return n != 0


def read_string(reader):
    return read_utf8(reader)


def read_object_property(reader, d):
    length = unpack('>H', reader.read(2))[0]
    if length == 0:
        reader.read(1)
        return d
    else:
        key = reader.read(length).decode()
        value = read_value_type(reader)
        d[key] = value
        return read_object_property(reader, d)


def read_reference(reader):
    return unpack('>H', reader.read(2))[0]


def read_ecma_array(reader):
    associative_count = unpack('>I', reader.read(4))[0]
    return [read_object_property(reader) for i in range(associative_count)]


def read_strict_array(reader):
    array_count = unpack('>I', reader.read(4))[0]
    return [read_value_type(reader) for i in range(array_count)]


def read_date(reader):
    date = unpack('>Q', reader.read(8))[0]
    time_zone = unpack('>h', reader.read(2))[0]
    return date, time_zone


def read_long_string(reader):
    return read_utf8_long(reader)


def read_xml_document(reader):
    return read_utf8_long(reader)


def read_typed_object(reader):
    class_name = read_utf8(reader)
    object_property = read_object_property(reader)
    return class_name, object_property


def read_value_type(reader):
    marker = reader.read(1)
    if marker == AMF0Marker.number:
        return read_number(reader)
    elif marker == AMF0Marker.boolean:
        return read_boolean(reader)
    elif marker == AMF0Marker.string:
        return read_utf8(reader)
    elif marker == AMF0Marker.object:
        return read_object_property(reader, {})
    elif marker == AMF0Marker.movieclip:
        return
    elif marker == AMF0Marker.null:
        return None
    elif marker == AMF0Marker.undefined:
        return None
    elif marker == AMF0Marker.reference:
        return read_reference(reader)
    elif marker == AMF0Marker.ecma_array:
        return read_ecma_array(reader)
    elif marker == AMF0Marker.object_end:
        return
    elif marker == AMF0Marker.strict_array:
        return read_strict_array(reader)
    elif marker == AMF0Marker.date:
        return read_date(reader)
    elif marker == AMF0Marker.long_string:
        return read_long_string(reader)
    elif marker == AMF0Marker.unsupported:
        return
    elif marker == AMF0Marker.recordset:
        return
    elif marker == AMF0Marker.xml_document:
        return read_xml_document(reader)
    elif marker == AMF0Marker.typed_object:
        return read_typed_object(reader)
    else:
        raise ValueError('marker not yet implemented: ', marker)
