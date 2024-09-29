# Main.py
import library
import DetectChars

if __name__ == "__main__":
    print("Hello, this is main program")
    print(library.check_plate("29B 12345"))
    print(DetectChars.loadKNNDataAndTrainKNN())