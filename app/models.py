# coding: utf-8
from sqlalchemy.orm import relationship

from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.String(50), primary_key=True)
    cucumber = db.Column(db.String(255), nullable=True)
    generic = db.Column(db.String(255), nullable=True)
    issue_id = db.Column(db.String(255), nullable=False)
    issue_jira_id = db.Column(db.String(255), nullable=True)
    test_repo = db.Column(db.String(255), nullable=True)
    project_id = db.Column(db.String(50), nullable=False)
    test_type_id = db.Column(db.String(50), db.ForeignKey('test_type.id'), nullable=True)
    test_steps = db.relationship('TestStep', backref='test_steps', lazy=True)
    test_type = db.relationship('TestType', backref='test_types', lazy=True)


class TestType(db.Model):
    __tablename__ = 'test_type'

    id = db.Column(db.String(50), primary_key=True)
    index = db.Column(db.Integer, nullable=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    kind = db.Column(db.String(255), nullable=True)
    order = db.Column(db.String(255), nullable=True)
    default = db.Column(db.String(255), nullable=True)
    project_setting_id = db.Column(db.String(255), nullable=True)


class TestStep(db.Model):
    __tablename__ = 'test_steps'

    id = db.Column(db.String(50), primary_key=True)
    data = db.Column(db.Text, nullable=True)
    result = db.Column(db.Text, nullable=True)
    customFields = db.Column(db.Text, nullable=True)
    attachments = db.Column(db.Text, nullable=True)
    index = db.Column(db.Integer, nullable=True)
    action = db.Column(db.Text, nullable=True)
    test_id = db.Column(db.String(50), db.ForeignKey('tests.id', ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=False)


"""
Many to many relationship
Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
Test Sets and Test Runs table
"""

test_testsets = db.Table('map_test_testsets',
                         db.Column('test_id', db.String(50), db.ForeignKey('tests.id'), primary_key=True),
                         db.Column('testset_id', db.String(50), db.ForeignKey('test_sets.id'), primary_key=True)
                         )


class TestSets(db.Model):
    __tablename__ = 'test_sets'
    id = db.Column(db.String(50), primary_key=True)
    tests = db.relationship('Test', secondary=test_testsets, lazy='subquery',
                            backref=db.backref('tests', lazy=True))
    name = db.Column(db.String(255), nullable=True)


"""
Many to many relationship
Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
Test Sets and Test Runs table
"""

test_test_executions = db.Table('map_test_executions',
                                db.Column('test_id', db.String(50), db.ForeignKey('tests.id'), primary_key=True),
                                db.Column('test_execution_id', db.String(50), db.ForeignKey('test_executions.id'),
                                          primary_key=True)
                                )


class TestExecutions(db.Model):
    __tablename__ = 'test_executions'
    id = db.Column(db.String(50), primary_key=True)
    tests = db.relationship('Test', secondary=test_test_executions, lazy='subquery',
                            backref=db.backref('test_execution_tests', lazy=True))
    name = db.Column(db.String(255), nullable=True)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
    show = db.Column(db.Boolean, default=0)
    duration = db.Column(db.Integer, default=5)
    status = db.Column(db.String(20), default='success')
    message = db.Column(db.String(500), nullable=False)
    dynamic = db.Column(db.Boolean, default=0)
    object = db.Column(db.String(255))


"""
Define table for handle run test execution
"""


class TestStatus(db.Model):
    __tablename__ = 'test_status'
    id = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(255), unique=True)
    type = db.Column(db.String(255))
    project_setting_id = db.Column(db.String(255), nullable=True)


class MapTestExec(db.Model):
    __tablename__ = 'map_test_exec'
    id = db.Column(db.String(50), primary_key=True)
    test_id = db.Column(db.String(50), db.ForeignKey('tests.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    exec_id = db.Column(db.String(50), db.ForeignKey('test_executions.id', ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=True)
    index = db.Column(db.Integer)
    status_id = db.Column(db.String(50), db.ForeignKey('test_status.id', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=True)
    comment = db.Column(db.Text, nullable=True)


class TestStepDetail(db.Model):
    __tablename__ = 'test_step_details'
    id = db.Column(db.String(50), primary_key=True)
    status_id = db.Column(db.String(50), db.ForeignKey('test_status.id', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=True)
    test_step_id = db.Column(db.String(50),
                             db.ForeignKey('test_steps.id', ondelete='CASCADE', onupdate='CASCADE'),
                             nullable=True)
    map_test_exec_id = db.Column(db.String(50),
                                 db.ForeignKey('map_test_exec.id', ondelete='CASCADE', onupdate='CASCADE'),
                                 nullable=True)
    comment = db.Column(db.Text, nullable=True)


class TestActivity(db.Model):
    __tablename__ = 'test_activity'
    id = db.Column(db.String(50), primary_key=True)
    map_test_exec_id = db.Column(db.String(50),
                                 db.ForeignKey('map_test_exec.id', ondelete='CASCADE', onupdate='CASCADE'),
                                 nullable=True)
    comment = db.Column(db.Text, nullable=True)
    status_change = db.Column(db.Text, nullable=True)
    jira_user_id = db.Column(db.Text, nullable=True)


class Defects(db.Model):
    __tablename__ = 'defects'
    id = db.Column(db.String(50), primary_key=True)
    map_test_exec_id = db.Column(db.String(50),
                                 db.ForeignKey('map_test_exec.id', ondelete='CASCADE', onupdate='CASCADE'),
                                 nullable=True)
    test_step_detail_id = db.Column(db.String(50),
                                    db.ForeignKey('test_step_details.id', ondelete='CASCADE', onupdate='CASCADE'),
                                    nullable=True)

    test_issue_key = db.Column(db.Text, nullable=True)
    test_issue_id = db.Column(db.Text, nullable=True)


class TestEvidence(db.Model):
    __tablename__ = 'test_evidence'
    id = db.Column(db.String(50), primary_key=True)
    map_test_exec_id = db.Column(db.String(50),
                                 db.ForeignKey('map_test_exec.id', ondelete='CASCADE', onupdate='CASCADE'),
                                 nullable=True)
    test_step_detail_id = db.Column(db.String(50),
                                    db.ForeignKey('test_step_details.id', ondelete='CASCADE', onupdate='CASCADE'),
                                    nullable=True)
    name_file = db.Column(db.Text, nullable=True)
    url_file = db.Column(db.Text, nullable=True)
