#include <iostream>
#include <fstream>
#include <complex>

// A helper function to write a 4-byte integer in little-endian format
void writeInt(std::ofstream &f, int value) {
    f.put((char)(value & 0xFF));
    f.put((char)((value >> 8) & 0xFF));
    f.put((char)((value >> 16) & 0xFF));
    f.put((char)((value >> 24) & 0xFF));
}

// A helper function to write a 2-byte integer in little-endian format
void writeShort(std::ofstream &f, short value) {
    f.put((char)(value & 0xFF));
    f.put((char)((value >> 8) & 0xFF));
}

int main() {
    // Image dimensions
    const int width = 400;
    const int height = 300;

    // Mandelbrot parameters
    // The area of the complex plane we are visualizing
    double minReal = -2.0;
    double maxReal = 0.0;
    double minImag = -.67;
    double maxImag = .67;

    // Maximum number of iterations per point
    const int MAX_ITER = 1000;

    // Prepare a buffer for the image: 24-bit RGB
    // Each pixel: 3 bytes (B, G, R)
    // Total size: width * height * 3
    unsigned char *pixels = new unsigned char[width * height * 3];

    // Compute the Mandelbrot set
    for (int y = 0; y < height; ++y) {
        double cy = minImag + (maxImag - minImag) * y / (height - 1);
        for (int x = 0; x < width; ++x) {
            double cx = minReal + (maxReal - minReal) * x / (width - 1);
            std::complex<double> c(cx, cy);
            std::complex<double> z(0, 0);

            int iteration = 0;
            while (iteration < MAX_ITER && std::abs(z) <= 2.0) {
                z = z * z + c;
                iteration++;
            }

            // Determine color
            // If we escaped, iteration < MAX_ITER
            // Simple grayscale: color ~ iteration count
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
    std::ofstream f("fractal.bmp", std::ios::out | std::ios::binary);
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

    // BMP rows are padded to multiples of 4 bytes. 
    // Our rows are width*3 bytes. If that isn't divisible by 4, we must pad.
    int rowSize = (width * 3 + 3) & ~3; // Round up to next multiple of 4
    int padding = rowSize - width * 3;

    // BMP stores pixels bottom-to-top
    for (int y = height - 1; y >= 0; --y) {
        int rowStart = y * width * 3;
        f.write((char*)&pixels[rowStart], width * 3);
        // write padding if needed
        for (int i = 0; i < padding; ++i) {
            f.put((char)0);
        }
    }

    f.close();
    delete[] pixels;

    std::cout << "fractal.bmp has been generated." << std::endl;
    return 0;
}
