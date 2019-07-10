# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: check_data.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import grpc_interfaces.google_protobuf_wrappers_cp_pb2 as google__protobuf__wrappers__cp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='check_data.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x10\x63heck_data.proto\x1a!google_protobuf_wrappers_cp.proto\"p\n\nThresholds\x12\x30\n\x07warning\x18\x01 \x01(\x0b\x32\x1f.google_cp.protobuf.DoubleValue\x12\x30\n\x07\x66\x61ilure\x18\x02 \x01(\x0b\x32\x1f.google_cp.protobuf.DoubleValue\"c\n\x0e\x43heckStatistic\x12!\n\x04type\x18\x01 \x01(\x0e\x32\x13.CheckStatisticType\x12\r\n\x05value\x18\x02 \x01(\x01\x12\x1f\n\nthresholds\x18\x03 \x01(\x0b\x32\x0b.Thresholds\"j\n\x0b\x43heckResult\x12\x1c\n\x06status\x18\x01 \x01(\x0e\x32\x0c.CheckStatus\x12\x18\n\x04type\x18\x02 \x01(\x0e\x32\n.CheckType\x12#\n\nstatistics\x18\x03 \x03(\x0b\x32\x0f.CheckStatistic*\xf3\x0b\n\x12\x43heckStatisticType\x12\"\n\x1e\x43HECK_STATISTIC_TYPE_UNDEFINED\x10\x00\x12\x32\n.CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_MAX\x10\x01\x12\x32\n.CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_AVG\x10\x02\x12;\n7CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_WINDOWED_AVG\x10\x03\x12\x31\n-CHECK_STATISTIC_TYPE_ECL_INNOVATION_AMBER_PCT\x10\x04\x12:\n6CHECK_STATISTIC_TYPE_ECL_INNOVATION_AMBER_WINDOWED_PCT\x10\x05\x12/\n+CHECK_STATISTIC_TYPE_ECL_INNOVATION_RED_PCT\x10\x06\x12\x38\n4CHECK_STATISTIC_TYPE_ECL_INNOVATION_RED_WINDOWED_PCT\x10\x07\x12+\n\'CHECK_STATISTIC_TYPE_ECL_FAIL_RATIO_PCT\x10\x08\x12\x34\n0CHECK_STATISTIC_TYPE_ECL_FAIL_RATIO_WINDOWED_PCT\x10\t\x12+\n\'CHECK_STATISTIC_TYPE_ECL_IMU_CONING_MAX\x10\n\x12+\n\'CHECK_STATISTIC_TYPE_ECL_IMU_CONING_AVG\x10\x0b\x12\x34\n0CHECK_STATISTIC_TYPE_ECL_IMU_CONING_WINDOWED_AVG\x10\x0c\x12:\n6CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_MAX\x10\r\x12:\n6CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_AVG\x10\x0e\x12\x43\n?CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_WINDOWED_AVG\x10\x0f\x12=\n9CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_MAX\x10\x10\x12=\n9CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_AVG\x10\x11\x12\x46\nBCHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_WINDOWED_AVG\x10\x12\x12\x42\n>CHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_ANGLE_ERROR_WINDOWED_AVG\x10\x13\x12\x45\nACHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_VELOCITY_ERROR_WINDOWED_AVG\x10\x14\x12\x45\nACHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_POSITION_ERROR_WINDOWED_AVG\x10\x15\x12\x35\n1CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_ANGLE_BIAS_AVG\x10\x16\x12>\n:CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_ANGLE_BIAS_WINDOWED_AVG\x10\x17\x12\x38\n4CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_VELOCITY_BIAS_AVG\x10\x18\x12\x41\n=CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_VELOCITY_BIAS_WINDOWED_AVG\x10\x19*\x92\x01\n\x0b\x43heckStatus\x12\x1a\n\x16\x43HECK_STATUS_UNDEFINED\x10\x00\x12\x15\n\x11\x43HECK_STATUS_PASS\x10\x01\x12\x18\n\x14\x43HECK_STATUS_WARNING\x10\x02\x12\x15\n\x11\x43HECK_STATUS_FAIL\x10\x03\x12\x1f\n\x1b\x43HECK_STATUS_DOES_NOT_APPLY\x10\x04*\xd1\x04\n\tCheckType\x12\x18\n\x14\x43HECK_TYPE_UNDEFINED\x10\x00\x12&\n\"CHECK_TYPE_ECL_MAGNETOMETER_STATUS\x10\x01\x12*\n&CHECK_TYPE_ECL_MAGNETIC_HEADING_STATUS\x10\x02\x12)\n%CHECK_TYPE_ECL_VELOCITY_SENSOR_STATUS\x10\x03\x12)\n%CHECK_TYPE_ECL_POSITION_SENSOR_STATUS\x10\x04\x12\'\n#CHECK_TYPE_ECL_HEIGHT_SENSOR_STATUS\x10\x05\x12\x34\n0CHECK_TYPE_ECL_HEIGHT_ABOVE_GROUND_SENSOR_STATUS\x10\x06\x12)\n%CHECK_TYPE_ECL_AIRSPEED_SENSOR_STATUS\x10\x07\x12)\n%CHECK_TYPE_ECL_SIDESLIP_SENSOR_STATUS\x10\x08\x12\'\n#CHECK_TYPE_ECL_IMU_VIBRATION_STATUS\x10\t\x12\"\n\x1e\x43HECK_TYPE_ECL_IMU_BIAS_STATUS\x10\n\x12.\n*CHECK_TYPE_ECL_IMU_OUTPUT_PREDICTOR_STATUS\x10\x0b\x12&\n\"CHECK_TYPE_ECL_OPTICAL_FLOW_STATUS\x10\x0c\x12&\n\"CHECK_TYPE_ECL_FILTER_FAULT_STATUS\x10\rb\x06proto3')
  ,
  dependencies=[google__protobuf__wrappers__cp__pb2.DESCRIPTOR,])

_CHECKSTATISTICTYPE = _descriptor.EnumDescriptor(
  name='CheckStatisticType',
  full_name='CheckStatisticType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_UNDEFINED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_MAX', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_AVG', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_WINDOWED_AVG', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_INNOVATION_AMBER_PCT', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_INNOVATION_AMBER_WINDOWED_PCT', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_INNOVATION_RED_PCT', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_INNOVATION_RED_WINDOWED_PCT', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_FAIL_RATIO_PCT', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_FAIL_RATIO_WINDOWED_PCT', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_CONING_MAX', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_CONING_AVG', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_CONING_WINDOWED_AVG', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_MAX', index=13, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_AVG', index=14, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_WINDOWED_AVG', index=15, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_MAX', index=16, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_AVG', index=17, number=17,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_WINDOWED_AVG', index=18, number=18,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_ANGLE_ERROR_WINDOWED_AVG', index=19, number=19,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_VELOCITY_ERROR_WINDOWED_AVG', index=20, number=20,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_POSITION_ERROR_WINDOWED_AVG', index=21, number=21,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_ANGLE_BIAS_AVG', index=22, number=22,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_ANGLE_BIAS_WINDOWED_AVG', index=23, number=23,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_VELOCITY_BIAS_AVG', index=24, number=24,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_VELOCITY_BIAS_WINDOWED_AVG', index=25, number=25,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=379,
  serialized_end=1902,
)
_sym_db.RegisterEnumDescriptor(_CHECKSTATISTICTYPE)

CheckStatisticType = enum_type_wrapper.EnumTypeWrapper(_CHECKSTATISTICTYPE)
_CHECKSTATUS = _descriptor.EnumDescriptor(
  name='CheckStatus',
  full_name='CheckStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATUS_UNDEFINED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATUS_PASS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATUS_WARNING', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATUS_FAIL', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_STATUS_DOES_NOT_APPLY', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1905,
  serialized_end=2051,
)
_sym_db.RegisterEnumDescriptor(_CHECKSTATUS)

CheckStatus = enum_type_wrapper.EnumTypeWrapper(_CHECKSTATUS)
_CHECKTYPE = _descriptor.EnumDescriptor(
  name='CheckType',
  full_name='CheckType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_UNDEFINED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_MAGNETOMETER_STATUS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_MAGNETIC_HEADING_STATUS', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_VELOCITY_SENSOR_STATUS', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_POSITION_SENSOR_STATUS', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_HEIGHT_SENSOR_STATUS', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_HEIGHT_ABOVE_GROUND_SENSOR_STATUS', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_AIRSPEED_SENSOR_STATUS', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_SIDESLIP_SENSOR_STATUS', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_IMU_VIBRATION_STATUS', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_IMU_BIAS_STATUS', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_IMU_OUTPUT_PREDICTOR_STATUS', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_OPTICAL_FLOW_STATUS', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHECK_TYPE_ECL_FILTER_FAULT_STATUS', index=13, number=13,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=2054,
  serialized_end=2647,
)
_sym_db.RegisterEnumDescriptor(_CHECKTYPE)

CheckType = enum_type_wrapper.EnumTypeWrapper(_CHECKTYPE)
CHECK_STATISTIC_TYPE_UNDEFINED = 0
CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_MAX = 1
CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_AVG = 2
CHECK_STATISTIC_TYPE_ECL_ESTIMATOR_FAILURE_WINDOWED_AVG = 3
CHECK_STATISTIC_TYPE_ECL_INNOVATION_AMBER_PCT = 4
CHECK_STATISTIC_TYPE_ECL_INNOVATION_AMBER_WINDOWED_PCT = 5
CHECK_STATISTIC_TYPE_ECL_INNOVATION_RED_PCT = 6
CHECK_STATISTIC_TYPE_ECL_INNOVATION_RED_WINDOWED_PCT = 7
CHECK_STATISTIC_TYPE_ECL_FAIL_RATIO_PCT = 8
CHECK_STATISTIC_TYPE_ECL_FAIL_RATIO_WINDOWED_PCT = 9
CHECK_STATISTIC_TYPE_ECL_IMU_CONING_MAX = 10
CHECK_STATISTIC_TYPE_ECL_IMU_CONING_AVG = 11
CHECK_STATISTIC_TYPE_ECL_IMU_CONING_WINDOWED_AVG = 12
CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_MAX = 13
CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_AVG = 14
CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_ANGLE_WINDOWED_AVG = 15
CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_MAX = 16
CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_AVG = 17
CHECK_STATISTIC_TYPE_ECL_IMU_HIGH_FREQ_DELTA_VELOCITY_WINDOWED_AVG = 18
CHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_ANGLE_ERROR_WINDOWED_AVG = 19
CHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_VELOCITY_ERROR_WINDOWED_AVG = 20
CHECK_STATISTIC_TYPE_ECL_IMU_OBSERVED_POSITION_ERROR_WINDOWED_AVG = 21
CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_ANGLE_BIAS_AVG = 22
CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_ANGLE_BIAS_WINDOWED_AVG = 23
CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_VELOCITY_BIAS_AVG = 24
CHECK_STATISTIC_TYPE_ECL_IMU_DELTA_VELOCITY_BIAS_WINDOWED_AVG = 25
CHECK_STATUS_UNDEFINED = 0
CHECK_STATUS_PASS = 1
CHECK_STATUS_WARNING = 2
CHECK_STATUS_FAIL = 3
CHECK_STATUS_DOES_NOT_APPLY = 4
CHECK_TYPE_UNDEFINED = 0
CHECK_TYPE_ECL_MAGNETOMETER_STATUS = 1
CHECK_TYPE_ECL_MAGNETIC_HEADING_STATUS = 2
CHECK_TYPE_ECL_VELOCITY_SENSOR_STATUS = 3
CHECK_TYPE_ECL_POSITION_SENSOR_STATUS = 4
CHECK_TYPE_ECL_HEIGHT_SENSOR_STATUS = 5
CHECK_TYPE_ECL_HEIGHT_ABOVE_GROUND_SENSOR_STATUS = 6
CHECK_TYPE_ECL_AIRSPEED_SENSOR_STATUS = 7
CHECK_TYPE_ECL_SIDESLIP_SENSOR_STATUS = 8
CHECK_TYPE_ECL_IMU_VIBRATION_STATUS = 9
CHECK_TYPE_ECL_IMU_BIAS_STATUS = 10
CHECK_TYPE_ECL_IMU_OUTPUT_PREDICTOR_STATUS = 11
CHECK_TYPE_ECL_OPTICAL_FLOW_STATUS = 12
CHECK_TYPE_ECL_FILTER_FAULT_STATUS = 13



_THRESHOLDS = _descriptor.Descriptor(
  name='Thresholds',
  full_name='Thresholds',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='warning', full_name='Thresholds.warning', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='failure', full_name='Thresholds.failure', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=55,
  serialized_end=167,
)


_CHECKSTATISTIC = _descriptor.Descriptor(
  name='CheckStatistic',
  full_name='CheckStatistic',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='CheckStatistic.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='CheckStatistic.value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='thresholds', full_name='CheckStatistic.thresholds', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=169,
  serialized_end=268,
)


_CHECKRESULT = _descriptor.Descriptor(
  name='CheckResult',
  full_name='CheckResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='CheckResult.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='CheckResult.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='statistics', full_name='CheckResult.statistics', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=270,
  serialized_end=376,
)

_THRESHOLDS.fields_by_name['warning'].message_type = google__protobuf__wrappers__cp__pb2._DOUBLEVALUE
_THRESHOLDS.fields_by_name['failure'].message_type = google__protobuf__wrappers__cp__pb2._DOUBLEVALUE
_CHECKSTATISTIC.fields_by_name['type'].enum_type = _CHECKSTATISTICTYPE
_CHECKSTATISTIC.fields_by_name['thresholds'].message_type = _THRESHOLDS
_CHECKRESULT.fields_by_name['status'].enum_type = _CHECKSTATUS
_CHECKRESULT.fields_by_name['type'].enum_type = _CHECKTYPE
_CHECKRESULT.fields_by_name['statistics'].message_type = _CHECKSTATISTIC
DESCRIPTOR.message_types_by_name['Thresholds'] = _THRESHOLDS
DESCRIPTOR.message_types_by_name['CheckStatistic'] = _CHECKSTATISTIC
DESCRIPTOR.message_types_by_name['CheckResult'] = _CHECKRESULT
DESCRIPTOR.enum_types_by_name['CheckStatisticType'] = _CHECKSTATISTICTYPE
DESCRIPTOR.enum_types_by_name['CheckStatus'] = _CHECKSTATUS
DESCRIPTOR.enum_types_by_name['CheckType'] = _CHECKTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Thresholds = _reflection.GeneratedProtocolMessageType('Thresholds', (_message.Message,), dict(
  DESCRIPTOR = _THRESHOLDS,
  __module__ = 'check_data_pb2'
  # @@protoc_insertion_point(class_scope:Thresholds)
  ))
_sym_db.RegisterMessage(Thresholds)

CheckStatistic = _reflection.GeneratedProtocolMessageType('CheckStatistic', (_message.Message,), dict(
  DESCRIPTOR = _CHECKSTATISTIC,
  __module__ = 'check_data_pb2'
  # @@protoc_insertion_point(class_scope:CheckStatistic)
  ))
_sym_db.RegisterMessage(CheckStatistic)

CheckResult = _reflection.GeneratedProtocolMessageType('CheckResult', (_message.Message,), dict(
  DESCRIPTOR = _CHECKRESULT,
  __module__ = 'check_data_pb2'
  # @@protoc_insertion_point(class_scope:CheckResult)
  ))
_sym_db.RegisterMessage(CheckResult)


# @@protoc_insertion_point(module_scope)
