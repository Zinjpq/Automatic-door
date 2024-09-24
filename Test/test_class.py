class Car:
    # Thuộc tính của class
    wheels = 4

    # Hàm khởi tạo
    def __init__(self, make, model, year):
        # Thuộc tính của đối tượng
        self.make = make
        self.model = model
        self.year = year

    # Phương thức của đối tượng
    def start_engine(self):
        print(f"Xe {self.make} {self.model} {self.year} đang khởi động!")

    # Phương thức của class
    @classmethod
    def display_wheels(cls):
        print(f"Mọi chiếc xe đều có {cls.wheels} bánh.")


# Tạo đối tượng Car
my_car = Car("Toyota", "Camry", 2020)

# Gọi phương thức của đối tượng
my_car.start_engine()

# Gọi phương thức của class
Car.display_wheels()


class ElectricCar(Car):
    def __init__(self, make, model, year, battery_size):
        # Gọi hàm khởi tạo của class cha
        super().__init__(make, model, year)
        self.battery_size = battery_size

    # Phương thức mới trong class con
    def battery_info(self):
        print(f"Xe {self.make} có pin {self.battery_size} kWh.")


my_electric_car = ElectricCar("Tesla", "Model 3", 2021, 75)
my_electric_car.start_engine()  # Phương thức kế thừa từ Car
my_electric_car.battery_info()  # Phương thức của ElectricCar

# class MyClass:
#     # Thuộc tính của class (Class attributes)
#     class_attribute = "Đây là thuộc tính của lớp"
#
#     # Hàm khởi tạo (Constructor)
#     def __init__(self, instance_attribute):
#         # Thuộc tính của đối tượng (Instance attributes)
#         self.instance_attribute = instance_attribute
#
#     # Phương thức (Method) của class
#     def print_info(self):
#         print(f"Thuộc tính của đối tượng: {self.instance_attribute}")
#         print(f"Thuộc tính của lớp: {MyClass.class_attribute}")
#
# # Tạo đối tượng (Instance) từ class
# my_object = MyClass("Giá trị của thuộc tính đối tượng")
#
# # Gọi phương thức của đối tượng
# my_object.print_info()
