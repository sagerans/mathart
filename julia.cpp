#include <iostream>
#include <fstream>
#include <complex>

// Helper function to write a 4-byte integer in little-endian format
static void writeInt(std::ofstream &f, int value) {
    f.put((char)(value & 0xFF));
    f.put((char)((value >> 8) & 0xFF));
    f.put((char)((value >> 16) & 0xFF));
    f.put((char)((value >> 24) & 0xFF));
}

// Helper function to write a 2-byte integer in little-endian format
static void writeShort(std::ofstream &f, short value) {
    f.put((char)(value & 0xFF));
    f.put((char)((value >> 8) & 0xFF));
}

int main() {
    // Image dimensions
    const int width = 400;
    const int height = 300;

    // Julia set parameters
    // Constant c for the Julia set
    std::complex<double> c(-0.7, 0.27015);

    // The area of the complex plane we are visualizing
    double minReal = -1.5;
    double maxReal = 1.5;
    double minImag = -1.0;
    double maxImag = 1.0;

    // Maximum number of iterations per point
    const int MAX_ITER = 1000;

    // Prepare a buffer for the image: 24-bit RGB
    unsigned char *pixels = new unsigned char[width * height * 3];

    // Compute the Julia set
    for (int y = 0; y < height; ++y) {
        double imagVal = minImag + (maxImag - minImag) * y / (height - 1);
        for (int x = 0; x < width; ++x) {
            double realVal = minReal + (maxReal - minReal) * x / (width - 1);
            std::complex<double> z(realVal, imagVal);

            int iteration = 0;
            while (iteration < MAX_ITER && std::abs(z) <= 2.0) {
                z = z * z + c;
                iteration++;
            }

            // Determine color
            unsigned char color = (unsigned char)(255.0 * iteration / MAX_ITER);

            // BMP expects BGR order
            unsigned char b = color;
            unsigned char g = color;
            unsigned char r = color;

            int index = (y * width + x) * 3;
            pixels[index + 0] = b;
            pixels[index + 1] = g;
            pixels[index + 2] = r;
        }
    }

    // Write out the BMP file
    std::ofstream f("julia_fractal.bmp", std::ios::out | std::ios::binary);
    if (!f) {
        std::cerr << "Could not open output file for writing." << std::endl;
        delete[] pixels;
        return 1;
    }

    // BMP file header
    // File header (14 bytes)
    f.put('B');
    f.put('M');
    int fileSize = 54 + (width * height * 3); // 54-byte header + pixel data
    writeInt(f, fileSize);
    writeInt(f, 0); // reserved
    writeInt(f, 54); // offset to pixel data (54 = 14 + 40)

    // DIB header (40 bytes)
    writeInt(f, 40); // DIB header size
    writeInt(f, width);
    writeInt(f, height);
    writeShort(f, 1);  // number of color planes
    writeShort(f, 24); // bits per pixel
    writeInt(f, 0);    // compression (no compression)
    writeInt(f, width * height * 3); // image size
    writeInt(f, 0); // horizontal resolution (pixel per meter) - not set
    writeInt(f, 0); // vertical resolution (pixel per meter) - not set
    writeInt(f, 0); // number of colors in palette
    writeInt(f, 0); // important colors

    // Compute row padding
    int rowSize = (width * 3 + 3) & ~3; 
    int padding = rowSize - width * 3;

    // BMP stores pixels bottom-to-top
    for (int y = height - 1; y >= 0; --y) {
        int rowStart = y * width * 3;
        f.write((char*)&pixels[rowStart], width * 3);
        for (int i = 0; i < padding; ++i) {
            f.put((char)0);
        }
    }

    f.close();
    delete[] pixels;

    std::cout << "julia_fractal.bmp has been generated." << std::endl;
    return 0;
}
