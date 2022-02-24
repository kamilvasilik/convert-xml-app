from xml.dom import minidom
import xml.etree.ElementTree as ET
import xmltodict
import os
import json


def create_detail(detail_root, data_detail):
    detail = ET.SubElement(detail_root, 'Detail')
    det_amount = ET.SubElement(detail, 'Amount')
    if 'item_amount_total' in data_detail.keys():
        det_amount.text = data_detail['item_amount_total']
    det_account_id = ET.SubElement(detail, 'AccountId')
    if 'account_id' in data_detail.keys():
        det_account_id.text = data_detail['account_id']
    det_quantity = ET.SubElement(detail, 'Quantity')
    if 'item_quantity' in data_detail.keys():
        det_quantity.text = data_detail['item_quantity']
    det_notes = ET.SubElement(detail, 'Notes')
    if 'item_description' in data_detail.keys():
        det_notes.text = data_detail['item_description'].replace('\n', ' ')


def create_payable(payable_root, data_main, data_details):
    payable = ET.SubElement(payable_root, 'Payable')

    invoice_number = ET.SubElement(payable, 'InvoiceNumber')
    if 'invoice_id' in data_main.keys():
        invoice_number.text = data_main['invoice_id']
    invoice_date = ET.SubElement(payable, 'InvoiceDate')
    if 'date_issue' in data_main.keys():
        invoice_date.text = data_main['date_issue']
    due_date = ET.SubElement(payable, 'DueDate')
    if 'date_due' in data_main.keys():
        due_date.text = data_main['date_due']
    total_amount = ET.SubElement(payable, 'TotalAmount')
    if 'amount_total' in data_main.keys():
        total_amount.text = data_main['amount_total']
    notes = ET.SubElement(payable, 'Notes')
    if 'notes' in data_main.keys():
        notes.text = data_main['notes']
    iban = ET.SubElement(payable, 'Iban')
    if 'iban' in data_main.keys():
        iban.text = data_main['iban']
    amount = ET.SubElement(payable, 'Amount')
    if 'amount_total_tax' in data_main.keys():
        amount.text = data_main['amount_total_tax']
    currency = ET.SubElement(payable, 'Currency')
    if 'currency' in data_main.keys():
        currency.text = data_main['currency']
    vendor = ET.SubElement(payable, 'Vendor')
    if 'sender_name' in data_main.keys():
        vendor.text = data_main['sender_name']
    vendor_address = ET.SubElement(payable, 'VendorAddress')
    if 'sender_address' in data_main.keys():
        vendor_address.text = data_main['sender_address'].replace('\n', ' ')
    details = ET.SubElement(payable, 'Details')
    for data_detail in data_details:
        create_detail(details, data_detail)


def convert_xml_file(xml_in_file, xml_out_file):
    tree = ET.parse(xml_in_file)
    root = tree.getroot()

    invoice_registers = ET.Element('InvoiceRegisters')
    invoices_element = ET.SubElement(invoice_registers, 'Invoices')

    invoices = root[0]

    annotation_id = invoices[0].attrib['url'].split('/')[-1]

    for invoice in invoices:
        invoice_content = invoice[7]
        data_main = {}
        data_details = []
        for section in invoice_content:
            if len(section) > 0:
                for datapoint in section:
                    if datapoint.text is None:
                        continue
                    data_main[datapoint.attrib['schema_id']] = datapoint.text

                if section.attrib['schema_id'] == 'line_items_section':
                    line_items = section[0]
                    for line_item in line_items:
                        detail_list = {}
                        for dp in line_item:
                            detail_list[dp.attrib['schema_id']] = dp.text
                        data_details.append(detail_list)

        create_payable(invoices_element, data_main, data_details)

    # xml to pretty xml and save file
    xml_to_str = ET.tostring(invoice_registers)
    xml_to_pretty_str = minidom.parseString(xml_to_str).toprettyxml(indent='  ')

    with open(xml_out_file, 'w') as f_out:
        f_out.write(xml_to_pretty_str)

    return annotation_id, xml_out_file


if __name__ == '__main__':
    xml_to_read_file = 'export-UK demo teplate-2021-03-08.xml'
    xml_to_write_file = 'converted_UK_file_out.xml'

    # xml_to_read_file = 'export-Received EU invoices-2022-02-21.xml'
    # xml_to_write_file = 'converted_EU_file_out.xml'

    annot_id, xml_file = convert_xml_file(xml_to_read_file, xml_to_write_file)
