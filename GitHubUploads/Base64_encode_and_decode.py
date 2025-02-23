import base64


# Function to encode a string to Base64
def encode_to_base64(data):
    # Convert the string to bytes
    encode_to_byte = data.encode('utf-8')
    # Encode the bytes to Base64
    encode_to_base64 = base64.b64encode(encode_to_byte)
    # Convert the Base64 bytes back to a string
    base64_string = encode_to_base64.decode('utf-8')
    return base64_string


def decode_to_ascii(data):

    # Convert the string to bytes
    encode_to_byte = data.encode('utf-8')
    # Encode the bytes to Base64
    decode_to_regular_bytes = base64.b64decode(encode_to_byte)
    # Convert the Base64 bytes back to a string
    decode_to_regular_string = decode_to_regular_bytes.decode('utf-8')
    return decode_to_regular_string


# Example usage
data = input('enter data you want to encode to base 64:')
encoded_data = encode_to_base64(data)

print(f"Original data: {data}")
print(f"Encoded to Base64: {encoded_data}")
print('===============================')
print('Now decoding to string:')
decoded_data=decode_to_ascii(encoded_data)
print(f"Base64 date data: {encoded_data}")
print(f"Decoded to to string: {decoded_data}")