# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: src/income_expense_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='src/income_expense_config.proto',
  package='beancount.income_expense',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1fsrc/income_expense_config.proto\x12\x18\x62\x65\x61ncount.income_expense\"c\n\x13IncomeExpenseConfig\x12\x17\n\x0f\x62udget_accounts\x18\x01 \x03(\t\x12\x33\n\x08mappings\x18\x02 \x03(\x0b\x32!.beancount.income_expense.Mapping\"\'\n\x07Mapping\x12\x0e\n\x06source\x18\x01 \x02(\t\x12\x0c\n\x04\x64\x65st\x18\x02 \x02(\t'
)




_INCOMEEXPENSECONFIG = _descriptor.Descriptor(
  name='IncomeExpenseConfig',
  full_name='beancount.income_expense.IncomeExpenseConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='budget_accounts', full_name='beancount.income_expense.IncomeExpenseConfig.budget_accounts', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mappings', full_name='beancount.income_expense.IncomeExpenseConfig.mappings', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=61,
  serialized_end=160,
)


_MAPPING = _descriptor.Descriptor(
  name='Mapping',
  full_name='beancount.income_expense.Mapping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='beancount.income_expense.Mapping.source', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dest', full_name='beancount.income_expense.Mapping.dest', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=162,
  serialized_end=201,
)

_INCOMEEXPENSECONFIG.fields_by_name['mappings'].message_type = _MAPPING
DESCRIPTOR.message_types_by_name['IncomeExpenseConfig'] = _INCOMEEXPENSECONFIG
DESCRIPTOR.message_types_by_name['Mapping'] = _MAPPING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IncomeExpenseConfig = _reflection.GeneratedProtocolMessageType('IncomeExpenseConfig', (_message.Message,), {
  'DESCRIPTOR' : _INCOMEEXPENSECONFIG,
  '__module__' : 'src.income_expense_config_pb2'
  # @@protoc_insertion_point(class_scope:beancount.income_expense.IncomeExpenseConfig)
  })
_sym_db.RegisterMessage(IncomeExpenseConfig)

Mapping = _reflection.GeneratedProtocolMessageType('Mapping', (_message.Message,), {
  'DESCRIPTOR' : _MAPPING,
  '__module__' : 'src.income_expense_config_pb2'
  # @@protoc_insertion_point(class_scope:beancount.income_expense.Mapping)
  })
_sym_db.RegisterMessage(Mapping)


# @@protoc_insertion_point(module_scope)
