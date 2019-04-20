#!/usr/bin/env python3
# coding: utf8

from controller.Controller import Controller
from controller.MemberController import MemberController

from test.test_functions import *


class MemberTest:
    nb_tests = 0
    nb_tests_succeed = 0

    @staticmethod
    def create_members():
        print('\033[01m## Creation ##\033[0m')

        make_test(lambda: MemberController.create_member({
            "password": "l33tP@ss",
            "firstName": "John",
            "lastName": "Connor",
            "email": "john.connor@terminator.com",
            "birthday": "1967-01-20",
            "gradeYear": 3,
            "telephone": 116316425,
            "positions": [{
                'id': 1,
                'year': 2014
            }, {
                'id': 3,
                'year': 2018
            }]
        }))(MemberTest, 'all needed attributes', False)

        make_test(lambda: MemberController.create_member({
            "password": "l33tP@ss",
            "firstName": "Louis",
            "lastName": "Rodolphe",
            "email": "louis.rodolphe@terminator.com",
            "birthday": "1967-01-20",
            "gradeYear": 3,
            "telephone": 116316425,
            "positions": [{
                'id': 2,
                'year': 2015
            }, {
                'id': 3,
                'year': 2017
            }]
        }))(MemberTest, 'all needed attributes', False)

        make_test(lambda: MemberController.create_member({
            "password": "l33tP@ss",
            "firstName": "Lucie",
            "lastName": "Connor",
            "email": "lucie.connor@terminator.com",
            "birthday": "1967-01-20",
            "gradeYear": 3,
            "telephone": 116316425
        }))(MemberTest, 'all needed attributes', False)

        '''make_test(lambda: MemberController.create_document({
            'title': 'title',
            'subject': 'Subject1',
            'type': 'type',
            'description': 'a description',
            'link': '1.gif'}))(
            MemberTest, 'all needed attributes', False)

        make_test(lambda: MemberController.create_document({
            'title': 'title',
            'subject': 'Subject2',
            'type': 'type',
            'description': 'a description',
            'link': '2.gif',
            'refDate': '2019-02-05'
        }))(MemberTest, 'all needed attributes', False)

        make_test(lambda: MemberController.create_document({
            'title': 'another title',
            'subject': 'Subject3',
            'type': 'type',
            'non_attr': 'non_value',
            'refDate': '2018-12-03',
            'description': 'an other description',
            'link': '3.png'
        }))(MemberTest, 'needed + nonexistent attributes', False)

        make_test(lambda: MemberController.create_document({
            'title': 'another title'
        }))(MemberTest, 'needed argument missing', True)
    '''
        
    @staticmethod
    def read_documents():
        print('\n\033[01m## Reading ##\033[0m')

        make_test(lambda: MemberController.get_members({}))(
            MemberTest, 'all documents', False)

        make_test(lambda: MemberController.get_members({
            'firstName': 'John'
        }))(
            MemberTest, 'specific documents', False)

        make_test(lambda: MemberController.get_member_by_id(2))(
            MemberTest, 'document with existing id', False)

        make_test(lambda: MemberController.get_member_by_id(-1))(
            MemberTest, 'document with non existing id', True)

    '''
    @staticmethod
    def update_documents():
        print('\n\033[01m## Updating ##\033[0m')
        make_test(lambda: MemberController.update_document(1, {
            'positionX': 12,
            'description': 'description of a document'
        }))(MemberTest, 'existing document', False)

        make_test(lambda: MemberController.update_document(1, {
            'positionX': 12,
            'description': 'another description'
        }))(MemberTest, 'existing document', False)

        make_test(lambda: MemberController.update_document(-1, {
            'positionX': 12,
            'description': 'description of a document'
        }))(MemberTest, 'existing document', True)
    '''

    @staticmethod
    def delete_documents():
        print('\n\033[01m## Deletion ##\033[0m')
        make_test(lambda: MemberController.delete_member(3))(
            MemberTest, 'existing document', False)

        make_test(lambda: MemberController.delete_member(3))(
            MemberTest, 'non existing document', True)


if __name__ == '__main__':
    Controller.recreate_tables()
    Controller.import_position()
    MemberTest.create_members()
    MemberTest.read_documents()
    # MemberTest.update_documents()
    MemberTest.read_documents()
    # MemberTest.delete_documents()
    MemberTest.read_documents()
    print('\n\n\033[04mSuccess\033[01m: ',
          MemberTest.nb_tests_succeed, '/',
          MemberTest.nb_tests, sep='')
