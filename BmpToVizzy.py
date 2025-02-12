import struct
import sys

def read_bmp(filename):
    with open(filename, 'rb') as f:
        file_header = f.read(14)
        info_header = f.read(40)
        
        if file_header[:2] != b'BM':
            print("File is not a BMP")
            return None, None, None
        
        bmp_width = struct.unpack('<I', info_header[4:8])[0]
        bmp_height = struct.unpack('<I', info_header[8:12])[0]
        
        pixels = []
        padding = (4 - (bmp_width * 3) % 4) % 4
        
        for y in range(bmp_height):
            row = []
            for x in range(bmp_width):
                color = struct.unpack('BBB', f.read(3))
                pixel_value = color[0] + (color[1] << 8) + (color[2] << 16)
                row.append(pixel_value)
            f.read(padding)
            pixels.extend(row)
        
        return bmp_width, bmp_height, pixels

def write_rle_pixels(filename, width, height, pixels):
    with open(filename, 'w') as f:
        print(f"Width is {width} pixels\nHeight is {height} pixels\nWriting pixel data to {filename}")
        f.write(f"{width},{height},1,")
        
        previous_color = pixels[0]
        count = 0
        max_index = len(pixels) - 1
        
        for index, color in enumerate(pixels):
            if previous_color != color or index == max_index:
                f.write(f"{previous_color:06X},{count}")
                if index < max_index:
                    f.write(",")
                previous_color = color
                count = 1
            else:
                count += 1

def write_raw_pixels(filename, width, height, pixels):
    with open(filename, 'w') as f:
        print(f"Width is {width} pixels\nHeight is {height} pixels\nWriting pixel data to {filename}")
        f.write(f"{width},{height},0,")
        
        f.write(",".join(f"{color:06X}" for color in pixels))

def main():
    if len(sys.argv) <= 1:
        print("Please include a 24-bit BMP file as an argument")
        return
    
    bmp_width, bmp_height, pixels = read_bmp(sys.argv[1])
    if pixels is None:
        return
    
    write_rle_pixels("RLE_Pixels.txt", bmp_width, bmp_height, pixels)
    write_raw_pixels("Raw_Pixels.txt", bmp_width, bmp_height, pixels)

if __name__ == "__main__":
    main()
