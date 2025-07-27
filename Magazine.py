import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QDialog, QSpinBox, QDialogButtonBox, QLabel, QComboBox

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
    def __init__(self, client, product, quantity):
        self.client = client
        self.product = product
        self.quantity = quantity
        self.total = product.price * quantity

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

        # Таблица заказов
        self.orderTable = QTableWidget()
        self.orderTable.setColumnCount(6)
        self.orderTable.setHorizontalHeaderLabels(['Клиент', 'ИНН', 'Товар', 'Цена','Количество', 'Сумма'])
        layout.addWidget(self.orderTable)

        # Кнопки для добавления клиентов, товаров и заказов
        self.viewClientsButton = QPushButton('Список клиентов')
        self.viewClientsButton.clicked.connect(self.openClientsList)
        layout.addWidget(self.viewClientsButton)

        self.addProductButton = QPushButton('Добавить товар')
        self.addProductButton.clicked.connect(self.openProductForm)
        layout.addWidget(self.addProductButton)

        self.addOrderButton = QPushButton('Добавить заказ')
        self.addOrderButton.clicked.connect(self.openOrderForm)
        layout.addWidget(self.addOrderButton)

        # Кнопка "Обновить"
        self.refreshButton = QPushButton('Обновить')
        self.refreshButton.clicked.connect(self.updateOrderTable)
        layout.addWidget(self.refreshButton)

        self.setMaximumSize(1200, 800)
        self.setMinimumSize(430, 400)

        self.setLayout(layout)

    def updateOrderTable(self):
            self.orderTable.setRowCount(len(self.orders))
            for i, order in enumerate(self.orders):
                # Если клиент был удалён, показываем строку вместо объекта клиента
                client_name = order.client if isinstance(order.client, str) else order.client.name
                client_inn = order.client.inn if not isinstance(order.client, str) else "Удален"
                self.orderTable.setItem(i, 0, QTableWidgetItem(client_name))
                self.orderTable.setItem(i, 1, QTableWidgetItem(client_inn))  # Отображаем ИНН клиента
                self.orderTable.setItem(i, 2, QTableWidgetItem(order.product.name))
                self.orderTable.setItem(i, 3, QTableWidgetItem(str(order.product.price)))  # Цена товара
                self.orderTable.setItem(i, 4, QTableWidgetItem(str(order.quantity)))  # Количество
                self.orderTable.setItem(i, 5, QTableWidgetItem(str(order.total)))  # Стоимость
            

    def openClientsList(self):
        dialog = ClientsListForm(self)
        dialog.exec_()

    def openProductForm(self):
        dialog = ProductForm(self)
        if dialog.exec_():
            name = dialog.productName.text()
            price = float(dialog.productPrice.text())
            self.products.append(Product(name, price))

    def openOrderForm(self):
        dialog = OrderForm(self)
        if dialog.exec_():
            client = dialog.client
            product = dialog.product
            quantity = dialog.quantity
            self.orders.append(Order(client, product, quantity))
            self.updateOrderTable()


class ClientForm(QDialog):
    def __init__(self, parent=None, client=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить клиента' if client is None else 'Редактировать клиента')

        self.clientName = QLineEdit(self)
        self.clientPhone = QLineEdit(self)

        if client:
            self.clientName.setText(client.name)
            self.clientPhone.setText(client.phone)

        layout = QFormLayout()
        layout.addRow('Имя клиента:', self.clientName)
        layout.addRow('Телефон клиента:', self.clientPhone)

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

        self.deleted_client_name = None

        # Обработка выбора клиента в таблице
        self.clientTable.selectionModel().selectionChanged.connect(self.onClientSelected)

    def populateClientTable(self):
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
            phone = dialog.clientPhone.text()
            self.parent().clients.append(Client(name, phone))
            self.populateClientTable()

    def openEditClientForm(self):
        selected_row = self.clientTable.selectedIndexes()[0].row()
        client = self.parent().clients[selected_row]
        dialog = ClientForm(self, client)
        if dialog.exec_():
            # Обновляем данные клиента по id
            client.name = dialog.clientName.text()
            client.phone = dialog.clientPhone.text()
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


class ProductForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить товар')

        self.productName = QLineEdit(self)
        self.productPrice = QLineEdit(self)

        layout = QFormLayout()
        layout.addRow('Название товара:', self.productName)
        layout.addRow('Цена товара:', self.productPrice)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

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

        self.productComboBox = QComboBox(self)
        for product in parent.products:
            self.productComboBox.addItem(product.name, product)  # Только имя товара отображается
        self.productComboBox.currentIndexChanged.connect(self.onProductChanged)

        # Устанавливаем первый товар по умолчанию
        self.productComboBox.setCurrentIndex(0)
        self.product = parent.products[0]  # Инициализируем товар

        self.quantitySpinBox = QSpinBox(self)
        self.quantitySpinBox.setRange(1, 100)

        layout = QFormLayout()
        layout.addRow('Клиент:', self.clientComboBox)
        layout.addRow('Товар:', self.productComboBox)
        layout.addRow('Количество:', self.quantitySpinBox)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.quantity = 1

    def onClientChanged(self, index):
        # Получаем объект клиента при изменении индекса
        self.client = self.clientComboBox.currentData()

    def onProductChanged(self, index):
        # Получаем объект товара при изменении индекса
        self.product = self.productComboBox.currentData()

    def accept(self):
        if self.client is None or self.product is None:
            # Покажем сообщение об ошибке, если клиент или товар не выбраны
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите клиента и товар для заказа.")
            return

        self.quantity = self.quantitySpinBox.value()
        super().accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())