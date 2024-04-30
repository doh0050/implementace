CREATE TABLE Person
(
 userID INTEGER NOT NULL,
 name VARCHAR2(30) NOT NULL,
 city VARCHAR2(30) NOT NULL,
 birth_year INTEGER NULL,
 email VARCHAR2(30) NULL,
 country VARCHAR2(30) NOT NULL,
 status INTEGER NOT NULL,
 CONSTRAINT PK_person PRIMARY KEY (userID)
)
;

CREATE TABLE Product
(
 productID INTEGER NOT NULL,
 category INTEGER NOT NULL,
 name VARCHAR2(30) NOT NULL,
 production_year INTEGER NOT NULL,
 current_price INTEGER NOT NULL,
 CONSTRAINT PK_Product PRIMARY KEY (productID)
)
;

CREATE TABLE Branch
(
 branchID INTEGER NOT NULL,
 city VARCHAR2(30) NOT NULL,
 status INTEGER NOT NULL,
 CONSTRAINT PK_branch PRIMARY KEY (branchID)
)
;

CREATE TABLE Employee
(
 employeeID INTEGER NOT NULL,
 branchID INTEGER NOT NULL,
 name VARCHAR2(30) NOT NULL,
 date_of_birth Date NOT NULL,
 pay_grade INTEGER NOT NULL,
 CONSTRAINT PK_employee PRIMARY KEY (employeeID),
 CONSTRAINT FK_employee_branch FOREIGN KEY (branchID) REFERENCES Branch(branchID)
)
;

CREATE TABLE Order
(
 orderID INTEGER NOT NULL,
 userID INTEGER NOT NULL,
 created TIMESTAMP NOT NULL,
 confirmed TIMESTAMP NULL,
 delivered TIMESTAMP NULL,
 employeeID INTEGER NOT NULL,
 CONSTRAINT PK_order PRIMARY KEY (orderID),
 CONSTRAINT FK_order_person FOREIGN KEY (userID) REFERENCES Person(userID),
 CONSTRAINT FK_order_employee FOREIGN KEY (employeeID) REFERENCES Employee(employeeID)
)
;

CREATE TABLE Item
(
 orderID INTEGER NOT NULL,
 productID INTEGER NOT NULL,
 price INTEGER NOT NULL,
 quantity INTEGER NOT NULL,
 CONSTRAINT PK_item PRIMARY KEY (orderID,productID),
 CONSTRAINT FK_item_order FOREIGN KEY (orderID) REFERENCES Order(orderID),
 CONSTRAINT FK_item_product FOREIGN KEY (productID) REFERENCES Product(productID)
)
;

CREATE TABLE Warehouse
(
 branchID INTEGER NOT NULL,
 productID INTEGER NOT NULL,
 quantity INTEGER NOT NULL,
 CONSTRAINT PK_warehouse PRIMARY KEY (branchID,productID),
 CONSTRAINT FK_warehouse_branch FOREIGN KEY (branchID) REFERENCES Branch(branchID),
 CONSTRAINT FK_warehouse_product FOREIGN KEY (productID) REFERENCES Product(productID)
)
;
