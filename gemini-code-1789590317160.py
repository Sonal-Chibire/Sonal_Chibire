import numpy as np
import plotly.graph_objects as go

# 1. Mesh Grid Setup
x = np.linspace(0, 10, 100)
y = np.linspace(-2, 2, 50)
X, Y = np.meshgrid(x, y)

# 2. Stress Field Calculations
bending_stress = (10 - X) * np.abs(Y)
fixed_singularity = 12 * np.exp(-((X - 0) ** 2 + (np.abs(Y) - 1.8) ** 2) / 0.15)
stress_idealized = bending_stress + fixed_singularity

compliance_levels = np.linspace(0.0, 1.0, 11)


def calculate_realistic_stress(comp):
    return bending_stress * (1 - comp * 0.5 * np.exp(-X / 2.5))


# 3. Create Interactive Figure with Subplots
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=(
        "Idealized Fixed Constraint (Artificial Corner Singularity)",
        "Realistic Compliant Support (Dynamic Load Path)",
    ),
    vertical_spacing=0.15,
)

# Top Trace: Fixed Idealized Constraint (Static)
fig.add_trace(
    go.Contour(
        z=stress_idealized,
        x=x,
        y=y,
        colorscale="Jet",
        zmin=0,
        zmax=25,
        colorbar=dict(title="Stress (MPa)", len=0.8),
        showscale=True,
    ),
    row=1,
    col=1,
)

# Bottom Traces: Compliant Support across 11 Slider Frames
for idx, comp in enumerate(compliance_levels):
    stress_real = calculate_realistic_stress(comp)
    fig.add_trace(
        go.Contour(
            z=stress_real,
            x=x,
            y=y,
            colorscale="Jet",
            zmin=0,
            zmax=25,
            showscale=False,
            visible=(idx == 4),  # Default active frame: compliance = 0.4
        ),
        row=2,
        col=1,
    )

# 4. Build Interactive Slider Steps
steps = []
num_static_traces = 1  # Trace 0 is the idealized plot

for idx, comp in enumerate(compliance_levels):
    # Visibility array: Keep trace 0 visible, toggle bottom traces
    visible_state = [True] + [False] * len(compliance_levels)
    visible_state[num_static_traces + idx] = True

    step = dict(
        method="update",
        args=[
            {"visible": visible_state},
            {
                "title.text": f"FEA Boundary Condition Study — Support Compliance: {comp:.2f}"
            },
        ],
        label=f"{comp:.1f}",
    )
    steps.append(step)

sliders = [
    dict(
        active=4,
        currentvalue={"prefix": "Support Compliance: "},
        pad={"t": 50},
        steps=steps,
    )
]

# 5. Layout Formatting
fig.update_layout(
    title=dict(
        text="FEA Boundary Condition Sensitivity Study",
        x=0.5,
        font=dict(size=18),
    ),
    sliders=sliders,
    height=700,
    width=900,
)

fig.update_xaxes(title_text="Beam Length (mm)", row=2, col=1)
fig.update_yaxes(title_text="Height (mm)", row=1, col=1)
fig.update_yaxes(title_text="Height (mm)", row=2, col=1)

# 6. Export Self-Contained Interactive HTML
fig.write_html("fea_sensitivity_interactive.html", include_plotlyjs="cdn")
print(
    "Successfully generated standalone file: 'fea_sensitivity_interactive.html'"
)