Basic Beer Tap display for 2 taps and Badger RP2040

For Badger 2040 e-Ink Display
Images must be 144x128 pixel with 1bit colour depth to fit side by side

You can use examples/badger2040/image_converter/convert.py to convert them:
   python3 convert.py --binary --resize image_file_1.png image_file_2.png image_file_3.png
Create a new "images" directory via Thonny, and upload the .bin files there.
   %Run convert.py --binary images/b1/Jupiler.png

Very Hacky !
