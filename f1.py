import matplotlib.pyplot as plt
import numpy as np
import fastf1.plotting

l
# Enable Matplotlib patches for plotting timedelta values and load
# FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False,
                          color_scheme='fastf1')

# load a session and its telemetry data
session = fastf1.get_session(2024, 'United States Grand Prix', 'R')
session.load()
ver_lap = session.laps.pick_drivers('1').pick_laps(52)
NOR_lap = session.laps.pick_drivers('4').pick_laps(52)
ver_tel = ver_lap.get_car_data().add_distance()
NOR_tel = NOR_lap.get_car_data().add_distance()
print(ver_lap['Team'])
rbr_color = fastf1.plotting.get_team_color(ver_lap['Team'].to_string(), session=session)
mer_color = fastf1.plotting.get_team_color(NOR_lap['Team'].to_string(), session=session)

fig, ax = plt.subplots()
ax.plot(ver_tel['Distance'], ver_tel['Brake'], color=rbr_color, label='VER')
ax.plot(NOR_tel['Distance'], NOR_tel['Brake'], color=mer_color, label='NOR')
circuit_info = session.get_circuit_info()
ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')
v_min = ver_tel['Brake'].min()
v_max = ver_tel['Brake'].max()
'''
ax.vlines(x=circuit_info.corners['Distance'], ymin=v_min, ymax=v_max,
          linestyles='dotted', colors='grey')
'''
'''
for _, corner in circuit_info.corners.iterrows():
    txt = f"{corner['Number']}{corner['Letter']}"
    ax.text(corner['Distance'], v_min, txt,
            va='center_baseline', ha='center', size='small')
'''
ax.set_xlim(3500,3800)
ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()
fig, ax = plt.subplots()
ax.plot(ver_tel['Distance'], ver_tel['Speed'], color=rbr_color, label='VER')
ax.plot(NOR_tel['Distance'], NOR_tel['Speed'], color=mer_color, label='NOR')
circuit_info = session.get_circuit_info()
ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')
v_min = ver_tel['Speed'].min()
v_max = ver_tel['Speed'].max()
'''
ax.vlines(x=circuit_info.corners['Distance'], ymin=v_min, ymax=v_max,
          linestyles='dotted', colors='grey')
'''
'''
for _, corner in circuit_info.corners.iterrows():
    txt = f"{corner['Number']}{corner['Letter']}"
    ax.text(corner['Distance'], v_min, txt,
            va='center_baseline', ha='center', size='small')
'''
ax.set_xlim(3500,3800)
ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()
fig, ax = plt.subplots()
ax.plot(ver_tel['Distance'], np.gradient(ver_tel['Speed']), color=rbr_color, label='VER')
ax.plot(NOR_tel['Distance'],  np.gradient(NOR_tel['Speed']), color=mer_color, label='NOR')
circuit_info = session.get_circuit_info()
ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')
v_min = ver_tel['Speed'].min()
v_max = ver_tel['Speed'].max()
'''
ax.vlines(x=circuit_info.corners['Distance'], ymin=v_min, ymax=v_max,
          linestyles='dotted', colors='grey')
'''
'''
for _, corner in circuit_info.corners.iterrows():
    txt = f"{corner['Number']}{corner['Letter']}"
    ax.text(corner['Distance'], v_min, txt,
            va='center_baseline', ha='center', size='small')
'''
ax.set_xlim(3500,3800)
ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()
