import oscP5.*;

final int OSC_PORT = 5005;

OscP5 oscP5;
float[] buffer;
float[] spectrum;
float peak;

void setup () {
  size(1025, 300);
  oscP5 = new OscP5(this, OSC_PORT);
}

void draw () {
  background(0);
  if (buffer != null) {
    stroke(#0000FF);
    drawArray(buffer);
  }
  if (spectrum != null) {
    stroke(127, 34, 255);
    drawArray(spectrum);
    float peakX = map(peak, 0, spectrum.length, 0, width);
    stroke(#FF0000);
    line(peakX, 0, peakX, height);
  }
}

void drawArray(float[] array) {
  for (int i = 0; i < array.length - 1; i++) {
    float x1 = map(i, 0, array.length, 0, width);
    float y1 = map(array[i], 0, 1023, height, 0);
    float x2 = map(i + 1, 0, array.length, 0, width);
    float y2 = map(array[i + 1], 0, 1023, height, 0);
    line(x1, y1, x2, y2);
  }
}

void oscEvent(OscMessage msg) {
  String address = msg.addrPattern();
  if (address.equals("/buffer")) {
    Object[] values = msg.arguments();
    buffer = new float[values.length];
    for (int i = 0; i < buffer.length; i++) {
      buffer[i] = (float) values[i];
    }
  }
  else if (address.equals("/spectrum")) {
    Object[] values = msg.arguments();
    spectrum = new float[values.length];
    for (int i = 0; i < spectrum.length; i++) {
      spectrum[i] = (float) values[i];
    }
  }
  else if (address.equals("/peak")) {
    peak = msg.get(0).floatValue();
  }
}