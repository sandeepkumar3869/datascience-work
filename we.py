import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import date, datetime
import calendar

# ------------------------------------------------------
# FUNCTION TO CREATE THE DASHBOARD BASED ON MONTH/YEAR
# ------------------------------------------------------
def create_landscape_dashboard(selected_year, selected_month):

    month_name = calendar.month_name[selected_month]
    n_days = calendar.monthrange(selected_year, selected_month)[1]

    fig = plt.figure(figsize=(11.69, 8.27), dpi=300)
    gs = gridspec.GridSpec(2, 1, height_ratios=[2.5, 1], hspace=0.25)

    # -----------------------
    # 1. MAIN HABIT TABLE
    # -----------------------
    ax1 = plt.subplot(gs[0])
    ax1.axis('off')

    plt.text(
        0.5, 1.12,
        f"Getting 1% Better Each Day - {month_name} {selected_year} Dashboard",
        ha='center',
        va='bottom',
        fontsize=20,
        fontweight='bold',
        transform=ax1.transAxes
    )

    n_habits = 12
    days = range(1, n_days + 1)

    col_labels = ["Protocols"] + [str(d) for d in days]

    w_proto = 0.18
    w_day = (1.0 - w_proto) / n_days
    col_widths = [w_proto] + [w_day] * n_days

    cell_text = [["" for _ in range(n_days + 1)] for _ in range(n_habits)]

    table1 = ax1.table(
        cellText=cell_text,
        colLabels=col_labels,
        colWidths=col_widths,
        loc="center",
        cellLoc="center"
    )

    table1.auto_set_font_size(False)
    table1.set_fontsize(10)
    table1.scale(1, 2.4)

    for key, cell in table1.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(fontweight="bold")
            cell.set_facecolor("#f0f0f0")
            cell.set_height(0.10)
        else:
            cell.set_height(0.09)

    # -----------------------
    # 2. SLEEP TABLE
    # -----------------------
    ax2 = plt.subplot(gs[1])
    ax2.axis("off")

    day_initials = []
    for d in range(1, n_days + 1):
        dt = date(selected_year, selected_month, d)
        mapping = {
            'Mon': 'M', 'Tue': 'T', 'Wed': 'W', 'Thu': 'Th',
            'Fri': 'F', 'Sat': 'Sa', 'Sun': 'Su'
        }
        day_initials.append(mapping.get(dt.strftime("%a"), ""))

    sleep_row_headers = ["Day", "8hrs", "7hrs", "6hrs", "5hrs", "4hrs"]

    sleep_data = []
    sleep_data.append([sleep_row_headers[0]] + day_initials)
    for label in sleep_row_headers[1:]:
        sleep_data.append([label] + ["" for _ in range(n_days)])

    sleep_col_labels = ["Sleep"] + [str(d) for d in days]

    table2 = ax2.table(
        cellText=sleep_data,
        colLabels=sleep_col_labels,
        colWidths=col_widths,
        loc="upper center",
        cellLoc="center"
    )

    table2.auto_set_font_size(False)
    table2.set_fontsize(10)
    table2.scale(1, 2.6)

    for key, cell in table2.get_celld().items():
        row, col = key
        if row == 0:
            cell.set_text_props(fontweight="bold")
            cell.set_facecolor("#f0f0f0")
            cell.set_height(0.10)
        else:
            cell.set_height(0.09)

        if col == 0:
            cell.set_text_props(fontweight="bold")

    # FINISHING TOUCHES
    fig.set_size_inches(11.69, 8.27)
    plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)

    return fig


# ------------------------------------------------------
# STREAMLIT INTERFACE
# ------------------------------------------------------

st.title("📊 Monthly Habit Dashboard Generator")

st.write("Select the month & year to instantly generate a print-ready tracker.")

year = st.selectbox("Year", list(range(2024, 2031)), index=1)
month = st.selectbox("Month", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])

if st.button("Generate Dashboard"):
    fig = create_landscape_dashboard(year, month)
    st.pyplot(fig)

    # Download Button
    filename = f"habit_tracker_{month}_{year}.png"
    fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.1)

    with open(filename, "rb") as f:
        st.download_button("Download PNG", data=f, file_name=filename)
