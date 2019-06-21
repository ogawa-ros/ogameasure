
import pymeasure

com = pymeasure.gpib_prologix('192.168.40.33', 30)
m = pymeasure.Lakeshore.model218(com)

all_ch = range(1, 9)


# alarm_query
# -----------
for i in all_ch:
    m.alarm_query(i)
    continue

m.alarm_query_all()

# alarm_set
# ---------
a = m.alarm_query(8)
m.alarm_set(8, 1, 1, 300, 100, 1, 0)
m.alarm_query(8)
m.alarm_set(8, *a)
m.alarm_query(8)

# alarm_status_query
# ------------------
for i in all_ch:
    m.alarm_status_query(1)
    continue

m.alarm_status_query_all()

# audible_alarm_query
# -------------------
m.audible_alarm_query()

# audible_alarm_set
# -----------------
m.audible_alarm_set(1)
m.audible_alarm_query()
m.audible_alarm_set(0)
m.audible_alarm_query()

# alarm_reset
# -----------
m.alarm_reset()

# analog_outputs_query
# --------------------
m.analog_outputs_query(1)
m.analog_outputs_query(2)

# analog_outputs_set
# ------------------
a = m.analog_outputs_query(1)
m.analog_outputs_set(1, 0, 1, 1, 1, 300, 3)
m.analog_outputs_query(1)

for i in [1,2,3,4,5]:
    m.analog_outputs_set(1, 0, mode=2, manual=i)
    m.analog_outputs_query(1)
    continue

m.analog_outputs_set(1, *a)
m.analog_outputs_query(1)

# analog_output_data_query
# ------------------------
m.analog_output_data_query(1)
m.analog_output_data_query(2)

# serial_interface_baud_rate_query
# --------------------------------
m.serial_interface_baud_rate_query()

# serial_interface_baud_rate_set
# ------------------------------
a = m.serial_interface_baud_rate_query()
m.serial_interface_baud_rate_set(1)
m.serial_interface_baud_rate_query()
m.serial_interface_baud_rate_set(2)
m.serial_interface_baud_rate_query()
m.serial_interface_baud_rate_set(a)
m.serial_interface_baud_rate_query()

# celsius_reading_query
# ---------------------
m.celsius_reading_query(0)
m.celsius_reading_query(1)
m.celsius_reading_query(2)

# curve_header_query
# ------------------
m.curve_header_query(21)
m.curve_header_query(22)
m.curve_header_query(23)

m.curve_header_query_all()

# curve_header_set
# ----------------
a = m.curve_header_query(28)
m.curve_header_set(28, 'TEST', 'TEST001', 2, 350, 1)
m.curve_header_query(28)
m.curve_header_set(28, *a)
m.curve_header_query(28)

# curve_point_query
# -----------------
m.curve_point_query(1, 1)
m.curve_point_query(1, 2)
m.curve_point_query(1, 3)

c1 = m.curve_point_query_line(1)
c2 = m.curve_point_query_line(2)

# import pylab
# pylab.plot(c1[0], c1[1])
# pylab.show()

# curve_point_set
# ---------------
c28 = m.curve_point_query_line(28)
m.curve_point_set(28, 1, 0, 10)
m.curve_point_query(28, 1)
m.curve_point_set(28, 2, 2, 15)
m.curve_point_query(28, 2)

m.curve_point_set_line(28, c1[0], c1[1])
c28_2 = m.curve_point_query_line(28)
m.curve_point_set_line(28, c28[0], c28[1])
c28_3 = m.curve_point_query_line(28)

# datetime_query
# --------------
m.datetime_query()

# datetime_set
# ------------
m.datetime_set(13, 12, 18, 17, 12, 0)
m.datetime_query()

m.datetime_set_now()
m.datetime_query()

# factory_defaults_reset
# ----------------------
m.factory_defaults_reset()

# display_field_query
# -------------------
m.display_field_query(1)
m.display_field_query(2)

m.display_field_query_all()

# display_field_set
# -----------------
a = m.display_field_query(8)
m.display_field_set(8, 1, 3)
m.display_field_query(8)
m.display_field_set(8, *a)
m.display_field_query(8)

m.display_field_set_all_kelvin()

# filter_query
# ------------
m.filter_query(1)
m.filter_query(2)
m.filter_query(3)

m.filter_query_all()

# filter_set
# ----------
a = m.filter_query(8)
m.filter_set(8, 1, 5, 2)
m.filter_query(8)
m.filter_set(8, *a)
m.filter_query(8)

# ieee488_query
# -------------
m.ieee488_query()

# ieee488_set
# -----------
a = m.ieee488_query()
m.ieee488_set()
m.ieee488_query()

# input_curve_query
# -----------------
m.input_curve_query(1)
m.input_curve_query(2)
m.input_curve_query(3)

m.input_curve_query_all()

# input_curve_set
# ---------------
a = m.input_curve_query(8)
m.input_curve_set(8, 28)
m.input_curve_query(8)
m.input_curve_set(8, 27)
m.input_curve_query(8)
m.input_curve_set(8, a)
m.input_curve_query(8)

# input_control_query
# -------------------
m.input_control_query(1)
m.input_control_query(2)
m.input_control_query(3)

m.input_control_query_all()

# input_control_set
# -----------------
a = m.input_control_query(8)
m.input_control_set(8, 1)
m.input_control_query(8)
m.input_control_set(8, 0)
m.input_control_query(8)
m.input_control_set(8, a)
m.input_control_query(8)

# input_type_query
# ----------------
m.input_type_query('A')
m.input_type_query('B')

m.input_type_query_all()

# input_type_set
# --------------
a = m.input_type_query('B')
m.input_type_set('B', 2)
m.input_type_query('B')
m.input_type_set('B', 3)
m.input_type_query('B')
m.input_type_set('B', a)
m.input_type_query('B')

# keypad_status_query
# -------------------
m.keypad_status_query()

# kelvin_reading_query
# --------------------
m.kelvin_reading_query(0)
m.kelvin_reading_query(1)
m.kelvin_reading_query(2)

# linear_equation_query
# ---------------------
m.linear_equation_query(1)
m.linear_equation_query(2)
m.linear_equation_query(3)

m.linear_equation_query_all()

# linear_equation_set
# -------------------
a = m.linear_equation_query(8)
m.linear_equation_set(8, 1, 1, 5)
m.linear_equation_query(8)
m.linear_equation_set(8, *a)
m.linear_equation_query(8)

# lockout_query
# -------------
m.lockout_query()

# lockout_set
# -----------
m.lockout_set(1, 123)
m.lockout_query()
m.lockout_set(0, 123)
m.lockout_query()

# logging_on_off_query
# --------------------
m.logging_on_off_query()

# logging_on_off
# --------------
m.logging_on_off(1)
m.logging_on_off_query()
m.logging_on_off(0)
m.logging_on_off_query()

# logging_number_query
# --------------------
m.logging_number_query()

# logging_records_query
# ---------------------
m.logging_records_query(1)
m.logging_records_query(2)
m.logging_records_query(3)

m.logging_records_query_all()

# logging_records_set
# -------------------
a = m.logging_records_query(7)
m.logging_records_set(7, 8, 1)
m.logging_records_query(7)
m.logging_records_set(7, *a)
m.logging_records_query(7)

# logging_parameter_query
# -----------------------
m.logging_parameter_query()

# logging_parameter_set
# ---------------------
a = m.logging_parameter_query()
m.logging_parameter_set(0, 1, 0, 10, 1)
m.logging_parameter_query()
m.logging_parameter_set(*a)
m.logging_parameter_query()

# log_data_query
# --------------
m.log_data_query(1, 1)

# linear_equation_input_data_query
# --------------------------------
m.linear_equation_input_data_query(0)
m.linear_equation_input_data_query(1)
m.linear_equation_input_data_query(2)

# minmax_query
# ------------
m.minmax_query(1)
m.minmax_query(2)
m.minmax_query(3)

# minmax_set
# ----------
m.minmax_set(8, 1)

# minmax_data_query
# -----------------
m.minmax_data_query(1)
m.minmax_data_query(2)
m.minmax_data_query(3)

# minmax_function_reset
# ---------------------
m.minmax_function_reset()

# local_remote_mode_query
# -----------------------
m.local_remote_mode_query()

# local_remote_mode_set
# ---------------------
m.local_remote_mode_set(0)
m.local_remote_mode_query()
m.local_remote_mode_set(1)
m.local_remote_mode_query()
m.local_remote_mode_set(2)
m.local_remote_mode_query()
m.local_remote_mode_set(1)
m.local_remote_mode_query()

# reading_status_query
# --------------------
m.reading_status_query(1)
m.reading_status_query(2)
m.reading_status_query(3)

# relay_query
# -----------
m.relay_query(1)
m.relay_query(2)
m.relay_query(3)

# relay_set
# ---------
m.relay_set(1, 0, 1, 0)
m.relay_query(1)

# relay_status_query
# ------------------
m.relay_status_query()

# softcal_curve_generate
# ----------------------

# sensor_units_reading_query
# --------------------------
m.sensor_units_reading_query(0)
m.sensor_units_reading_query(1)
m.sensor_units_reading_query(2)

