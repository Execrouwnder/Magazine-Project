import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QDialog, QSpinBox, QDialogButtonBox, QLabel, QComboBox
import random
import string
from datetime import datetime




class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return self.name  # Это то, что будет отображаться в ComboBox

class Client:
    id_counter = 1  # Счётчик для генерации уникальных id

    def __init__(self, name, inn):
        self.id = Client.id_counter  # Присваиваем уникальный id
        Client.id_counter += 1  # Увеличиваем счётчик для следующего клиента
        self.name = name
        self.inn = inn  # ИНН

    def __str__(self):
        return self.name  # Это то, что будет отображаться в ComboBox

class Order:
    def __init__(self, client, products, quantity_list, order_number, date):
        self.client = client
        self.products = products  # Список товаров
        self.quantity_list = quantity_list  # Список количеств товаров
        self.order_number = order_number  # Номер заказа
        self.date = date  # Дата заказа
        self.total = sum(product.price * quantity for product, quantity in zip(products, quantity_list))  # Итоговая стоимость заказа

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.clients = []
        self.products = []
        self.orders = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Система учета заказов')

        layout = QVBoxLayout()

        self.orderTable = QTableWidget()
        self.orderTable.setColumnCount(4)
        self.orderTable.setHorizontalHeaderLabels(['Номер заказа', 'Дата', 'Клиент', 'Итоговая сумма'])
        self.orderTable.cellDoubleClicked.connect(self.openOrderDetails)
        layout.addWidget(self.orderTable)


        # Кнопки для добавления клиентов, товаров и заказов
        self.viewClientsButton = QPushButton('Список клиентов')
        self.viewClientsButton.clicked.connect(self.openClientsList)
        layout.addWidget(self.viewClientsButton)

        # Кнопка для открытия списка товаров
        self.viewProductsButton = QPushButton('Список товаров')
        self.viewProductsButton.clicked.connect(self.openProductList)
        layout.addWidget(self.viewProductsButton)

        self.addOrderButton = QPushButton('Добавить заказ')
        self.addOrderButton.clicked.connect(self.openOrderForm)
        layout.addWidget(self.addOrderButton)

        # Кнопка "Обновить"
        self.refreshButton = QPushButton('Обновить')
        self.refreshButton.clicked.connect(self.updateOrderTable)
        layout.addWidget(self.refreshButton)

        # Кнопка "Добавить тестовые данные"
        self.addTestDataButton = QPushButton('Добавить тестовые данные')
        self.addTestDataButton.clicked.connect(self.addTestData)
        layout.addWidget(self.addTestDataButton)

        self.setMaximumSize(1200, 800)
        self.setMinimumSize(430, 400)

        self.setLayout(layout)
    def addTestData(self):
         # Создаем тестовые товары и добавляем их в список товаров
        product_a = Product("Товар A", 100)
        product_b = Product("Товар B", 150)
        product_c = Product("Товар C", 200)

        self.products.extend([product_a, product_b, product_c])  # Добавляем товары в список

        # Создаем тестовых клиентов и добавляем их в список клиентов
        client_1 = Client("Клиент 1", "1234567890")
        client_2 = Client("Клиент 2", "0987654321")

        self.clients.extend([client_1, client_2])  # Добавляем клиентов в список
        


        # Создаем заказы с номером и датой
        order_1 = Order(client_1, [product_a], [2], 
                        ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)), datetime.now().strftime('%Y-%m-%d'))  # 2 штуки товара A
        order_2 = Order(client_2, [product_b, product_c], [1, 3], 
                        ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)), datetime.now().strftime('%Y-%m-%d'))  # 1 штука товара B и 3 штуки товара C

        # Добавляем заказы в список заказов
        self.orders.append(order_1)
        self.orders.append(order_2)

        # Обновляем таблицу с заказами
        self.updateOrderTable()

    def updateOrderTable(self):
        self.orderTable.setRowCount(len(self.orders))
        for i, order in enumerate(self.orders):
            client_name = order.client if isinstance(order.client, str) else order.client.name
            self.orderTable.setItem(i, 0, QTableWidgetItem(order.order_number))  # Номер заказа
            self.orderTable.setItem(i, 1, QTableWidgetItem(order.date))  # Дата
            self.orderTable.setItem(i, 2, QTableWidgetItem(client_name))  # Клиент
            self.orderTable.setItem(i, 3, QTableWidgetItem(str(order.total)))  # Итоговая сумма
            

    def openClientsList(self):
        dialog = ClientsListForm(self)
        dialog.exec_()  # Открываем форму списка клиентов

    def openProductList(self):
        dialog = ProductListForm(self)
        dialog.exec_()

    def openOrderDetails(self, row, column):
        order = self.orders[row]
        dialog = OrderDetailsForm(self, order)  # Открываем форму с деталями заказа
        dialog.exec_()

    def openOrderForm(self):
        dialog = OrderForm(self)
        if dialog.exec_():
            # Мы больше не добавляем заказ вручную здесь. Добавление заказа происходит внутри метода createOrder
            self.updateOrderTable()


class ClientForm(QDialog):
    def __init__(self, parent=None, client=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить клиента' if client is None else 'Редактировать клиента')

        self.clientName = QLineEdit(self)
        self.clientINN = QLineEdit(self)

        if client:
            self.clientName.setText(client.name)
            self.clientINN.setText(client.inn)

        layout = QFormLayout()
        layout.addRow('Имя клиента:', self.clientName)
        layout.addRow('ИНН Клиента:', self.clientINN)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)
        self.setLayout(layout)

class ClientsListForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Список клиентов')

        layout = QVBoxLayout()

        # Таблица клиентов
        self.clientTable = QTableWidget()
        self.clientTable.setColumnCount(2)
        self.clientTable.setHorizontalHeaderLabels(['Имя клиента', 'Телефон'])
        self.populateClientTable()
        layout.addWidget(self.clientTable)

        # Кнопки для добавления, редактирования и удаления клиента
        self.addClientButton = QPushButton('Добавить клиента')
        self.addClientButton.clicked.connect(self.openClientForm)
        layout.addWidget(self.addClientButton)

        self.editClientButton = QPushButton('Редактировать клиента')
        self.editClientButton.setEnabled(False)  # Выключено по умолчанию
        self.editClientButton.clicked.connect(self.openEditClientForm)
        layout.addWidget(self.editClientButton)

        self.deleteClientButton = QPushButton('Удалить клиента')
        self.deleteClientButton.setEnabled(False)  # Выключено по умолчанию
        self.deleteClientButton.clicked.connect(self.deleteClient)
        layout.addWidget(self.deleteClientButton)

        
        self.setLayout(layout)

        self.populateClientTable()

        self.deleted_client_name = None

        # Обработка выбора клиента в таблице
        self.clientTable.selectionModel().selectionChanged.connect(self.onClientSelected)

    def populateClientTable(self):
        # Очищаем таблицу перед обновлением данных
        self.clientTable.setRowCount(0)
        
        # Заполняем таблицу актуальными данными о клиентах
        self.clientTable.setRowCount(len(self.parent().clients))
        for i, client in enumerate(self.parent().clients):
            self.clientTable.setItem(i, 0, QTableWidgetItem(client.name))  # Имя клиента
            self.clientTable.setItem(i, 1, QTableWidgetItem(client.inn))   # ИНН клиента
            

    def onClientSelected(self):
        selected_row = self.clientTable.selectedIndexes()
        if selected_row:
            self.editClientButton.setEnabled(True)
            self.deleteClientButton.setEnabled(True)
        else:
            self.editClientButton.setEnabled(False)
            self.deleteClientButton.setEnabled(False)

    def openClientForm(self):
        dialog = ClientForm(self)
        if dialog.exec_():
            name = dialog.clientName.text()
            phone = dialog.clientINN.text()
            self.parent().clients.append(Client(name, phone))
            self.populateClientTable()

    def openEditClientForm(self):
        selected_row = self.clientTable.selectedIndexes()[0].row()
        client = self.parent().clients[selected_row]
        dialog = ClientForm(self, client)
        if dialog.exec_():
            # Обновляем данные клиента по id
            client.name = dialog.clientName.text()
            client.phone = dialog.clientINN.text()
            self.populateClientTable()

    def deleteClient(self):
        selected_row = self.clientTable.selectedIndexes()[0].row()
        client_to_delete = self.parent().clients[selected_row]

        # Сохраняем имя удалённого клиента
        self.deleted_client_name = client_to_delete.name

        # Удаляем клиента из списка
        del self.parent().clients[selected_row]

        # Заменяем клиента в заказах на "Удален <Имя клиента>"
        for order in self.parent().orders:
            if order.client == client_to_delete:
                order.client = f"Удален <{self.deleted_client_name}>"

        # Обновляем таблицу
        self.populateClientTable()

class ProductListForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Список товаров')

        layout = QVBoxLayout()

        # Таблица товаров
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(2)
        self.productTable.setHorizontalHeaderLabels(['Название товара', 'Цена'])
        self.populateProductTable()
        layout.addWidget(self.productTable)

        # Кнопки для добавления, редактирования и удаления товара
        self.addProductButton = QPushButton('Добавить товар')
        self.addProductButton.clicked.connect(self.openAddProductForm)
        layout.addWidget(self.addProductButton)

        self.editProductButton = QPushButton('Редактировать товар')
        self.editProductButton.setEnabled(False)  # Выключено по умолчанию
        self.editProductButton.clicked.connect(self.openEditProductForm)
        layout.addWidget(self.editProductButton)

        self.deleteProductButton = QPushButton('Удалить товар')
        self.deleteProductButton.setEnabled(False)  # Выключено по умолчанию
        self.deleteProductButton.clicked.connect(self.deleteProduct)
        layout.addWidget(self.deleteProductButton)

        self.setLayout(layout)

        self.deleted_product_name = None

        # Обработка выбора товара в таблице
        self.productTable.selectionModel().selectionChanged.connect(self.onProductSelected)

    def populateProductTable(self):
        self.productTable.setRowCount(len(self.parent().products))
        for i, product in enumerate(self.parent().products):
            self.productTable.setItem(i, 0, QTableWidgetItem(product.name))  # Название товара
            self.productTable.setItem(i, 1, QTableWidgetItem(str(product.price)))  # Цена товара

    def onProductSelected(self):
        selected_row = self.productTable.selectedIndexes()
        if selected_row:
            # Проверяем, используется ли товар в заказах
            product = self.parent().products[selected_row[0].row()]
            if self.isProductInOrders(product):
                self.deleteProductButton.setEnabled(False)  # Если товар используется, блокируем кнопку
            else:
                self.deleteProductButton.setEnabled(True)  # Иначе кнопку можно нажать
            self.editProductButton.setEnabled(True)
        else:
            self.editProductButton.setEnabled(False)
            self.deleteProductButton.setEnabled(False)

    def isProductInOrders(self, product):
        # Проверяем, используется ли товар в каких-либо заказах
        for order in self.parent().orders:
            if product.name in [p.name for p in order.products]:
                return True
        return False

    def openAddProductForm(self):
        dialog = ProductForm(self)
        if dialog.exec_():
            name = dialog.productName.text()
            price = float(dialog.productPrice.text())
            self.parent().products.append(Product(name, price))
            self.populateProductTable()

    def openEditProductForm(self):
        selected_row = self.productTable.selectedIndexes()[0].row()
        product = self.parent().products[selected_row]
        dialog = ProductForm(self, product)
        if dialog.exec_():
            # Обновляем данные товара
            product.name = dialog.productName.text()
            product.price = float(dialog.productPrice.text())
            self.populateProductTable()

            # После редактирования товара обновляем все заказы
            self.updateOrders()

    def deleteProduct(self):
        selected_row = self.productTable.selectedIndexes()[0].row()
        product_to_delete = self.parent().products[selected_row]

        # Сохраняем имя удалённого товара
        self.deleted_product_name = product_to_delete.name

        # Удаляем товар из списка
        del self.parent().products[selected_row]

        # Заменяем товар в заказах на "Удален <Имя товара>"
        for order in self.parent().orders:
            for i, product in enumerate(order.products):
                if product == product_to_delete:
                    order.products[i] = f"Удален <{self.deleted_product_name}>"

        # Обновляем таблицу товаров
        self.populateProductTable()
        # Обновляем таблицу заказов после удаления товара
        self.updateOrders()

    def updateOrders(self):
        # Пересчитываем итоговую сумму для каждого заказа
        for order in self.parent().orders:
            order.total = sum(product.price * quantity for product, quantity in zip(order.products, order.quantity_list))

        # Обновляем таблицу заказов
        self.parent().updateOrderTable()

class ProductForm(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить товар' if product is None else 'Редактировать товар')

        self.productName = QLineEdit(self)
        self.productPrice = QLineEdit(self)

        if product:
            self.productName.setText(product.name)
            self.productPrice.setText(str(product.price))

        layout = QFormLayout()
        layout.addRow('Название товара:', self.productName)
        layout.addRow('Цена товара:', self.productPrice)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)
        self.setLayout(layout)

class OrderDetailsForm(QDialog):
    def __init__(self, parent, order):
        super().__init__(parent)
        self.setWindowTitle('Детали заказа')

        self.order = order

        layout = QVBoxLayout()

        # Информация о заказе
        # Проверяем, является ли order.client строкой (если клиент удалён)
        if isinstance(order.client, str) and order.client.startswith("Удален"):
            client_name = order.client
            client_inn = "Удален"
        else:
            client_name = order.client.name
            client_inn = order.client.inn

        order_info = QLabel(f'Номер заказа: {order.order_number}\nДата: {order.date}\nКлиент: {client_name}\nИНН: {client_inn}\nИтоговая сумма: {order.total}')
        layout.addWidget(order_info)

        # Таблица товаров в заказе
        productTable = QTableWidget()
        productTable.setColumnCount(4)
        productTable.setHorizontalHeaderLabels(['Товар', 'Цена', 'Количество', 'Стоимость'])

        # Заполнение таблицы товарами
        productTable.setRowCount(len(order.products))
        for i, (product, quantity) in enumerate(zip(order.products, order.quantity_list)):
            productTable.setItem(i, 0, QTableWidgetItem(product.name))
            productTable.setItem(i, 1, QTableWidgetItem(str(product.price)))
            productTable.setItem(i, 2, QTableWidgetItem(str(quantity)))
            productTable.setItem(i, 3, QTableWidgetItem(str(product.price * quantity)))

        layout.addWidget(productTable)

        # Кнопки закрытия
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self)
        buttonBox.accepted.connect(self.accept)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

class OrderForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Создание заказа')

        self.clientComboBox = QComboBox(self)
        for client in parent.clients:
            self.clientComboBox.addItem(client.name, client)  # Только имя клиента отображается, но объект сохраняется
        self.clientComboBox.currentIndexChanged.connect(self.onClientChanged)

        # Устанавливаем первый элемент по умолчанию
        self.clientComboBox.setCurrentIndex(0)
        self.client = parent.clients[0]  # Инициализируем клиента

        # Генерация номера заказа и даты только в OrderForm
        self.order_number = self.generate_order_number()  # Генерация номера заказа
        self.order_date = datetime.now().strftime('%Y-%m-%d')  # Текущая дата

        # Лейблы для отображения номера заказа и даты
        self.orderNumberLabel = QLabel(f"Номер заказа: {self.order_number}")
        self.orderDateLabel = QLabel(f"Дата: {self.order_date}")

        # Таблица товаров в заказе
        self.productTable = QTableWidget()
        self.productTable.setColumnCount(4)
        self.productTable.setHorizontalHeaderLabels(['Товар', 'Цена', 'Количество', 'Стоимость'])

        # Кнопка для добавления товара
        self.addProductButton = QPushButton('Добавить товар')
        self.addProductButton.clicked.connect(self.openAddProductForm)

        # Кнопка для завершения создания заказа
        self.createOrderButton = QPushButton('Создать заказ')
        self.createOrderButton.clicked.connect(self.createOrder)

        layout = QVBoxLayout()
        layout.addWidget(self.clientComboBox)
        layout.addWidget(self.orderNumberLabel)
        layout.addWidget(self.orderDateLabel)
        layout.addWidget(self.productTable)
        layout.addWidget(self.addProductButton)
        layout.addWidget(self.createOrderButton)

        self.setLayout(layout)

        self.selected_products = []  # Список добавленных товаров
        self.quantity_list = []  # Список количеств товаров

    def onClientChanged(self, index):
        # Получаем объект клиента при изменении индекса
        self.client = self.clientComboBox.currentData()

    def openAddProductForm(self):
        # Передаем список товаров в форму для добавления товара
        dialog = AddProductForm(self, self.parent().products)  # Передаем список товаров
        if dialog.exec_():
            product = dialog.selected_product
            quantity = dialog.selected_quantity

            # Добавляем товар в таблицу и список
            if product and quantity:
                self.selected_products.append(product)
                self.quantity_list.append(quantity)
                self.updateProductTable()

    def updateProductTable(self):
        # Обновляем таблицу с товарами
        self.productTable.setRowCount(len(self.selected_products))
        for i, (product, quantity) in enumerate(zip(self.selected_products, self.quantity_list)):
            self.productTable.setItem(i, 0, QTableWidgetItem(product.name))
            self.productTable.setItem(i, 1, QTableWidgetItem(str(product.price)))
            self.productTable.setItem(i, 2, QTableWidgetItem(str(quantity)))
            self.productTable.setItem(i, 3, QTableWidgetItem(str(product.price * quantity)))

    def createOrder(self):
        # Проверяем, что в заказе есть хотя бы один товар
        if not self.selected_products:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, добавьте хотя бы один товар в заказ.")
            return

        # Создаем заказ с номером и датой, передаваемыми из формы
        order = Order(self.client, self.selected_products, self.quantity_list, self.order_number, self.order_date)

        # Добавляем заказ в список заказов
        self.parent().orders.append(order)

        # Обновляем таблицу заказов
        self.parent().updateOrderTable()

        self.accept()  # Закрываем окно после создания заказа

    def generate_order_number(self):
        # Генерация уникального номера заказа
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
class AddProductForm(QDialog):
    def __init__(self, parent=None, products=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить товар')

        self.selected_product = None
        self.selected_quantity = 1

        # Комбобокс для выбора товара
        self.productComboBox = QComboBox(self)
        for product in products:  # Используем переданный список товаров
            self.productComboBox.addItem(product.name, product)  # Отображаем имя товара

        # Селект для выбора количества
        self.quantitySpinBox = QSpinBox(self)
        self.quantitySpinBox.setRange(1, 100)

        # Кнопки для подтверждения
        self.addButton = QPushButton('Добавить', self)
        self.addButton.clicked.connect(self.accept)

        self.cancelButton = QPushButton('Отмена', self)
        self.cancelButton.clicked.connect(self.reject)

        layout = QFormLayout()
        layout.addRow('Товар:', self.productComboBox)
        layout.addRow('Количество:', self.quantitySpinBox)
        layout.addWidget(self.addButton)
        layout.addWidget(self.cancelButton)

        self.setLayout(layout)

    def accept(self):
        # Сохраняем выбранные товар и количество
        self.selected_product = self.productComboBox.currentData()
        self.selected_quantity = self.quantitySpinBox.value()

        super().accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())