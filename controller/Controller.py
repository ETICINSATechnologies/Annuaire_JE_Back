#!/usr/bin/env python3
# coding: utf8

import re
import pandas as pd

from controller.MemberController import MemberController
from util.Exception import FormatError
from util.db_config import *
from entities.User import User
from entities.Member import Member
from entities.MemberPosition import MemberPosition
from entities.Position import Position
import persistence_unit.PersistenceUnit as pUnit
from persistence_unit.PersistenceUnit import engine


class Controller:
    """
    Class that allows communication with the DB
    No instance is needed because all its methods are static.
    This methods are used to make a CRUD operation,
    by making a query or a transaction with the DB by using
    the decorators '~persistence_unit.PersistenceUnit.make_a_query'
    and make_a_transaction
    """

    @staticmethod
    def recreate_tables():
        Base.metadata.drop_all(pUnit.engine)
        Base.metadata.create_all(pUnit.engine)
        Controller.create_admin()

    @staticmethod
    def create_tables():
        Base.metadata.create_all(pUnit.engine)
        Controller.create_admin()

    @staticmethod
    @pUnit.make_a_transaction
    def create_admin(session):
        admin_exist = session.query(User).filter(
            User.username == 'admin').scalar() is not None
        if not admin_exist:
            user = User('admin')
            user.update(VarConfig.get()["password"])
            session.add(user)

    @staticmethod
    def import_position():
        Controller.recreate_tables()
        data = pd.read_excel('upload/annuaire.xlsx',
                             sheet_name='Positions')

        data['id'] = data.index + 1
        data = data.rename(columns={'position': 'label'})

        data.to_sql(name='position', con=engine, if_exists='append',
                    index=False)

    @staticmethod
    def import_data(file):
        if not re.match(r'\w*\.(xlsx|xlsm)', file.filename):
            raise FormatError

        excel_file = pd.ExcelFile(file)
        position = pd.read_excel(excel_file, sheet_name='Positions')

        position['id'] = position.index + 1
        position = position.rename(columns={'position': 'label'})

        member = pd.read_excel(excel_file, sheet_name='Members')
        member = member.rename(columns={
            'prénom': 'firstName',
            'nom': 'lastName',
            'genre': 'gender',
            'anniversaire': 'birthday',
            'année diplôme': 'gradeYear'
        })
        member.index += 2  # id 1 is for the admin
        member['id'] = member.index
        max_position_nb = len(
            member.filter(like='position').columns.values)

        m_positions_df = [
            member.filter(['id', f'position{i}', f'year{i}']).rename(
                columns={
                    'id': 'member_id',
                    f'position{i}': 'position',
                    f'year{i}': 'year'
                }
            )
            for i in range(1, max_position_nb + 1)
        ]

        member = member.drop(list(member.filter(
            regex='year\d|position\d')), axis=1)

        member['username'] = member['email'].apply(
            lambda x: x.split('@')[0])

        m_position = pd.concat(m_positions_df, ignore_index=True)

        used_positions = m_position.dropna()['position'].values
        for i in used_positions:
            if i not in position['label'].values:
                raise FormatError

        m_position = m_position.merge(
            position, left_on='position', right_on='label'
        )

        m_position = m_position.filter(['member_id', 'id', 'year'])

        Controller.recreate_tables()

        position.to_sql(name='position', con=engine, if_exists='append',
                        index=False)

        for mb in member.to_dict('records'):
            # remove null value
            mb = {k: v for k, v in mb.items() if not pd.isna(v)}
            # filter the member's positions
            m_pos = m_position.loc[m_position['member_id'] == mb['id']]
            mb['positions'] = \
                m_pos.filter(['id', 'year']).to_dict('records')

            MemberController.create_member(mb)

    @staticmethod
    def export_data():
        member_position = pd.read_sql(
            f'SELECT "user".id, member_position.year,'
            f' position.label as position '
            f'FROM "user"'
            f'  INNER JOIN member_position'
            f'    ON "user".id = member_position.member_id'
            f'  INNER JOIN position'
            f'    ON member_position.position_id = position.id', engine)

        m_position_id = [[], [], [], []]
        m_position_label = [[], [], [], []]
        m_position_year = [[], [], [], []]

        for i in list(set(member_position['id'])):
            # filter member_position with the id 'i'
            m_position = member_position[member_position.id == i]

            # each row corresponds to one position
            for index, row in enumerate(m_position.iterrows()):
                m_position_id[index].append(row[1]['id'])
                m_position_label[index].append(row[1]['position'])
                m_position_year[index].append(row[1]['year'])

        m_positions = [pd.DataFrame({
            'id': m_position_id[i],
            f'position{i+1}': m_position_label[i],
            f'year{i+1}': m_position_year[i]
        }) for i in range(4)]

        join_m_positions = m_positions[0]

        for i in range(1, len(m_positions)):
            join_m_positions = join_m_positions.merge(
                m_positions[i], on='id', how='outer')

        members = pd.read_sql('SELECT * FROM member', engine)
        position = pd.read_sql(
            'SELECT label as position FROM position', engine)

        members = members.merge(join_m_positions, on='id', how='outer')
        members = members.drop(list(members.filter(
            regex='id|username')), axis=1)

        with pd.ExcelWriter('upload/annuaire.xlsx') as writer:
            members.to_excel(writer, sheet_name='Members', index=False)
            position.to_excel(
                writer, sheet_name='Positions', index=False)


if __name__ == '__main__':
    Controller.recreate_tables()
