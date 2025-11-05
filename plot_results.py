import re
import plotly.graph_objects as go

def parse_log_file(filename):
    with open(filename, 'r') as f:
        text = f.read()

    data = {"NO SOFTMAX": [], "WITH SOFTMAX": []}
    current_section = None

    for line in text.splitlines():
        if "NO SOFTMAX" in line:
            current_section = "NO SOFTMAX"
        elif "WITH SOFTMAX" in line:
            current_section = "WITH SOFTMAX"

        elif line.startswith("eps="):
            eps = float(line.split('=')[1])
            data[current_section].append({"eps": eps})

        elif "analysis precision" in line:
            match = re.search(r"analysis precision\s+(\d+)\s*/\s*(\d+)", line)
            if match:
                verified, total = int(match.group(1)), int(match.group(2))
                precision = 100 * verified / total
                data[current_section][-1]["precision"] = precision

        elif "time:" in line:
            # extract the third float (total time)
            match = re.findall(r"[\d.]+", line)
            # if len(match) >= 3:
            runtime = float(match[-1])
            data[current_section][-1]["runtime"] = runtime

    return data


def plot_results(data):
    eps_no = [d["eps"] for d in data["NO SOFTMAX"]]
    eps_yes = [d["eps"] for d in data["WITH SOFTMAX"]]

    prec_no = [d["precision"] for d in data["NO SOFTMAX"]]
    prec_yes = [d["precision"] for d in data["WITH SOFTMAX"]]

    runtime_no = [d["runtime"] for d in data["NO SOFTMAX"]]
    runtime_yes = [d["runtime"] for d in data["WITH SOFTMAX"]]

    # --- Precision Plot ---
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=eps_no, y=prec_no, mode='lines+markers',
                              name='No Softmax', line=dict(color='royalblue', width=3)))
    fig1.add_trace(go.Scatter(x=eps_yes, y=prec_yes, mode='lines+markers',
                              name='With Softmax', line=dict(color='firebrick', width=3, dash='dash')))
    fig1.update_layout(
        # title="Verification Precision vs Epsilon",
        title=dict(
        text="Verification Precision vs Epsilon",
        x=0.5,  # centers the title horizontally
        xanchor='center'
    ),


        xaxis_title="ε (Perturbation Radius)",
        yaxis_title="Precision (%)",
        template="plotly_white",
        font=dict(size=14)
    )

    # --- Runtime Plot ---
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=eps_no, y=runtime_no, mode='lines+markers',
                              name='No Softmax', line=dict(color='royalblue', width=3)))
    fig2.add_trace(go.Scatter(x=eps_yes, y=runtime_yes, mode='lines+markers',
                              name='With Softmax', line=dict(color='firebrick', width=3, dash='dash')))
    fig2.update_layout(
        # title="Runtime vs Epsilon",
        title=dict(
        text="Runtime vs Epsilon",
        x=0.5,  # centers the title horizontally
        xanchor='center'
    ),
        xaxis_title="ε (Perturbation Radius)",
        yaxis_title="Runtime (seconds)",
        template="plotly_white",
        font=dict(size=14)
    )

    fig1.update_layout(legend=dict(
        orientation="v",
        yanchor="auto",
        y=0.5,
        xanchor="right",  # changed
        x=0.5
        ))
    fig2.update_layout(legend=dict(
        orientation="v",
        yanchor="auto",
        y=0.5,
        xanchor="right",  # changed
        x=0.5
        ))

    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(showgrid=False)
    fig2.update_xaxes(showgrid=False)
    fig2.update_yaxes(showgrid=False)

    # fig1.show()
    # fig2.show()
    fig1.write_image("./verification.png", scale=5)
    fig2.write_image("./runtime.png", scale=5)




import re
import pandas as pd
import plotly.graph_objects as go

def parse_failure_case(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    eps_list = []
    failure_case_list = []
    eps = None
    
    for line in lines:
        if match := re.search(r'eps=(\d+\.\d+)', line):
            eps = float(match.group(1))
        elif 'Exp failure_case Fallback' in line:
            failure_case = int(re.search(r'(\d+)', line.split(':')[1]).group(1))
            eps_list.append(eps)
            failure_case = failure_case / 1960
            failure_case_list.append(failure_case)
    
    return pd.DataFrame({'eps': eps_list, 'failure_case': failure_case_list})

def plot_tier():
    # Read data
    df_failure_case = parse_failure_case("evaluation_results.txt")

    # Line plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_failure_case['eps'], y=df_failure_case['failure_case'], mode='lines+markers', name='Tier 4 Calls'))

    fig.update_layout(
        title='Failure case calls vs Epsilon',
        title_x=0.5,  # center title
        xaxis_title='Epsilon',
        yaxis_title='Failure cases (%)',
        width=600,
        height=600
    )


    # fig.show()
    fig.write_image("./tiers.png", scale=5)




if __name__ == "__main__":
    data = parse_log_file("evaluation_results.txt")  # replace with your filename
    plot_results(data)
    plot_tier()