-- Create database
CREATE DATABASE IF NOT EXISTS ecochain_db;
USE ecochain_db;

-- Create vendors table
CREATE TABLE IF NOT EXISTS vendors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    country VARCHAR(100),
    carbon_score INT,
    compliance_status VARCHAR(50)
);

-- Create invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT,
    amount DECIMAL(15, 2),
    tax DECIMAL(15, 2),
    date DATE,
    status VARCHAR(50),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id) ON DELETE CASCADE
);

-- Create audit_logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    agent_name VARCHAR(100),
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert realistic sample data for vendors
INSERT IGNORE INTO vendors (id, name, industry, country, carbon_score, compliance_status) VALUES
(1, 'GlobalTech Supplies', 'Technology', 'USA', 85, 'Compliant'),
(2, 'EcoPaper Corp', 'Manufacturing', 'Canada', 92, 'Compliant'),
(3, 'FastShip Logistics', 'Transportation', 'UK', 60, 'Under Review'),
(4, 'SteelWorks Inc', 'Construction', 'Germany', 45, 'Non-Compliant'),
(5, 'GreenEnergy Solutions', 'Energy', 'Sweden', 98, 'Compliant');

-- Insert realistic sample data for invoices
INSERT IGNORE INTO invoices (id, vendor_id, amount, tax, date, status) VALUES
(101, 1, 5000.00, 500.00, '2023-01-15', 'Paid'),
(102, 1, 2500.00, 250.00, '2023-02-20', 'Paid'),
(103, 2, 12000.00, 1200.00, '2023-03-10', 'Pending'),
(104, 3, 800.00, 80.00, '2023-03-25', 'Paid'),
(105, 4, 45000.00, 4500.00, '2023-04-05', 'Pending'),
(106, 5, 3200.00, 320.00, '2023-04-12', 'Paid');
