from flask import Flask, request
import os 
import random
app = Flask(__name__)
pid = str(os.getpid())
rand = str(random.randint(0,100000))
@app.get("/")
def get_color():
    x = request.args.get("x")
    y = request.args.get("y")
    return {
        "x": x, 
        "y": y,
        "value": str(mandelbrot_set(int(x), int(y))),
        "Pid": pid + ":" + rand
    }

MAX_ITER = 80
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1

WIDTH = 680
HEIGHT = 440

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1
    return n


def mandelbrot_set(x, y):
    # Convert pixel coordinate to complex number
    c = complex(RE_START + (int(x) / WIDTH) * (RE_END - RE_START), IM_START + (int(y) / HEIGHT) * (IM_END - IM_START))
    # Compute the number of iterations
    m = mandelbrot(c)
    # The color depends on the number of iterations
    color = 255 - int(m * 255 / MAX_ITER)
    # Plot the point
    return (color, color, color)


if __name__ == '__main__':
    app.run(debug=True, port=6969)
