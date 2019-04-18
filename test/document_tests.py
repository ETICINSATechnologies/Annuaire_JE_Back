#!/usr/bin/env python3
# coding: utf8

from controller.Controller import Controller
from controller.DocController import DocController

from test.test_functions import *


class DocumentTest:
    nb_tests = 0
    nb_tests_succeed = 0

    # @TODO: create a method to check the success of uploading a file

    @staticmethod
    def create_documents():
        print('\033[01m## Creation ##\033[0m')

        make_test(lambda: DocController.create_document({
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif'
        }))(DocumentTest, 'all needed attributes', False)

        make_test(lambda: DocController.create_document({
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif'}))(
            DocumentTest, 'all needed attributes', False)

        make_test(lambda: DocController.create_document({
            'title': 'title',
            'subject': 'Subject2',
            'type': 'type',
            'description': 'a description',
            'link': '2.gif',
            'refDate': '2019-02-05'
        }))(DocumentTest, 'all needed attributes', False)

        make_test(lambda: DocController.create_document({
            'title': 'another title',
            'subject': 'Subject3',
            'type': 'type',
            'non_attr': 'non_value',
            'refDate': '2018-12-03',
            'description': 'an other description',
            'link': '3.png'
        }))(DocumentTest, 'needed + nonexistent attributes', False)

        make_test(lambda: DocController.create_document({
            'title': 'another title'
        }))(DocumentTest, 'needed argument missing', True)

    @staticmethod
    def read_documents():
        print('\n\033[01m## Reading ##\033[0m')

        make_test(lambda: DocController.get_documents({}))(
            DocumentTest, 'all documents', False)

        make_test(lambda: DocController.get_documents({
            'keyword': 'description',
            'refDateStart': '2018-12-03'
        }))(DocumentTest, 'specific documents', False)

        make_test(lambda: DocController.get_document_by_id(1))(
            DocumentTest, 'document with existing id', False)

        make_test(lambda: DocController.get_document_by_id(-1))(
            DocumentTest, 'document with non existing id', True)

    @staticmethod
    def update_documents():
        print('\n\033[01m## Updating ##\033[0m')
        make_test(lambda: DocController.update_document(1, {
            'positionX': 12,
            'description': 'description of a document'
        }))(DocumentTest, 'existing document', False)

        make_test(lambda: DocController.update_document(1, {
            'positionX': 12,
            'description': 'another description'
        }))(DocumentTest, 'existing document', False)

        make_test(lambda: DocController.update_document(-1, {
            'positionX': 12,
            'description': 'description of a document'
        }))(DocumentTest, 'existing document', True)

    @staticmethod
    def delete_documents():
        print('\n\033[01m## Deletion ##\033[0m')
        make_test(lambda: DocController.delete_documents(2))(
            DocumentTest, 'existing document', False)

        make_test(lambda: DocController.delete_documents(2))(
            DocumentTest, 'non existing document', True)


if __name__ == '__main__':
    Controller.recreate_tables()
    DocumentTest.create_documents()
    DocumentTest.read_documents()
    DocumentTest.update_documents()
    DocumentTest.read_documents()
    DocumentTest.delete_documents()
    DocumentTest.read_documents()
    print('\n\n\033[04mSuccess\033[01m: ',
          DocumentTest.nb_tests_succeed, '/',
          DocumentTest.nb_tests, sep='')
