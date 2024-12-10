-- Create database in RDS
Create Database Sales;

-- Create table command

CREATE TABLE customer_subscription (
    CustomerID INT,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    PlanType ENUM('Postpaid', 'Prepaid'),
    MonthlyCharge INT,
    SubscriptionDate DATE,
    PRIMARY KEY (CustomerID)
);