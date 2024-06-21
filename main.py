import pyfair
from pyfair import FairModel
import warnings
import streamlit as st
from decimal import Decimal
import pandas as pd
from io import BytesIO

warnings.simplefilter(action="ignore", category=FutureWarning)


def lm_display(model_number: int):
    st.write("Loss Magnitude (£ million)")
    results_args[f"lm_low_{model_number}"] = float(
        Decimal(
            st.number_input(
                label=f"LM LOW {model_number}",
                label_visibility="collapsed",
                step=0.1,
                min_value=0.0,
                max_value=None,
                value=0.1,
                placeholder="Loss Magnatude - Low"
            )
        )
        * Decimal(1000000.00)
    )
    results_args[f"lm_mode_{model_number}"] = float(
        Decimal(
            st.number_input(
                label=f"LM MODE {model_number}",
                label_visibility="collapsed",
                step=0.1,
                min_value=0.0,
                max_value=None,
                value=0.5,
                placeholder="Loss Magnatude - Mode"
            )
        )
        * Decimal(1000000.00)
    )
    results_args[f"lm_high_{model_number}"] = float(
        Decimal(
            st.number_input(
                label=f"LM high {model_number}",
                label_visibility="collapsed",
                step=0.1,
                min_value=0.0,
                max_value=None,
                value=1.0,
                placeholder="Loss Magnatude - High"
            )
        )
        * Decimal(1000000.00)
    )


def tef_display(model_number: int):
    st.write("TEF (per year)")
    results_args[f"tef_low_{model_number}"] = st.number_input(
        label=f"TEF low {model_number}",
        label_visibility="collapsed",
        step=1,
        min_value=0,
        max_value=None,
        value=2,
        placeholder="TEF - Low"
    )
    results_args[f"tef_mode_{model_number}"] = st.number_input(
        label=f"TEF mode {model_number}",
        label_visibility="collapsed",
        step=1,
        min_value=0,
        max_value=None,
        value=5,
        placeholder="TEF - Mode"
    )
    results_args[f"tef_high_{model_number}"] = st.number_input(
        label=f"TEF HIGH {model_number}",
        label_visibility="collapsed",
        step=1,
        min_value=0,
        max_value=None,
        value=12,
        placeholder="TEF - High"
    )


def contact_display(model_number: int):
    st.write("Contact Frequency (per year)")
    results_args[f"contact_low_{model_number}"] = st.number_input(
        label=f"Contact low {model_number}",
        label_visibility="collapsed",
        step=1,
        min_value=0,
        max_value=None,
        value=2,
        placeholder="Contact - Low"
    )
    results_args[f"contact_mode_{model_number}"] = st.number_input(
        label=f"Contact mode {model_number}",
        label_visibility="collapsed",
        step=1,
        min_value=0,
        max_value=None,
        value=5,
        placeholder="Contact - Mode"
    )
    results_args[f"contact_high_{model_number}"] = st.number_input(
        label=f"Contact high {model_number}",
        label_visibility="collapsed",
        step=1,
        min_value=0,
        max_value=None,
        value=20,
        placeholder="Contact - High"
    )


def vuln_display(model_number):
    st.write("Vulnerability (% per year)")
    results_args[f"vuln_low_{model_number}"] = st.number_input(
        label=f"VULN low {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        placeholder="Vulnerability - Low"
    )
    results_args[f"vuln_mode_{model_number}"] = st.number_input(
        label=f"VULN MODE {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        placeholder="Vulnerability - Mode"
    )
    results_args[f"vuln_high_{model_number}"] = st.number_input(
        label=f"VULN high {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        placeholder="Vulnerability - High"
    )


def action_display(model_number):
    st.write("Probability of Action (%)")
    results_args[f"action_low_{model_number}"] = st.number_input(
        label=f"Action low {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.1,
        placeholder="Probability of Action - Low"
    )
    results_args[f"action_mode_{model_number}"] = st.number_input(
        label=f"Action mode {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.15,
        placeholder="Probability of Action - Mode"
    )
    results_args[f"action_high_{model_number}"] = st.number_input(
        label=f"Action high {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.2,
        placeholder="Probability of Action - High"
    )


def threat_display(model_number):
    st.write("Threat Capacity (%)")
    results_args[f"threat_low_{model_number}"] = st.number_input(
        label=f"threat low {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.50,
        placeholder="Threat Capacity - Low"
    )
    results_args[f"threat_mode_{model_number}"] = st.number_input(
        label=f"threat mode {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.70,
        placeholder="Threat Capacity - Mode"
    )
    results_args[f"threat_high_{model_number}"] = st.number_input(
        label=f"threat high {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.90,
        placeholder="Threat Capacity - High"
    )


def control_display(model_number):
    st.write("Control Strength (%)")
    results_args[f"control_low_{model_number}"] = st.number_input(
        label=f"control low {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.70,
        placeholder="Control Strength - Low"
    )
    results_args[f"control_mode_{model_number}"] = st.number_input(
        label=f"control mode {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.80,
        placeholder="Control Strength - Mode"
    )
    results_args[f"control_high_{model_number}"] = st.number_input(
        label=f"control high {model_number}",
        label_visibility="collapsed",
        step=0.01,
        min_value=0.00,
        max_value=1.00,
        value=0.90,
        placeholder="Control Strength - High"
    )


def calculate_risk(simulations, use_tef, use_vuln, two_model, meta_model, **kwargs):
    """
    Calculates risk using PyFair models based on user input.

    Returns:
        - fsr (FairSimpleReport): PyFair report object
        - model1 (FairModel): First risk model
        - model2 (FairModel): Optional second risk model
        - mm (FairMetaModel): Optional meta model
    """
    # --- Model Creation and Input Handling ---
    model1 = create_fair_model(
        name="Risk Type 1",
        use_tef=use_tef,
        use_vuln=use_vuln,
        simulations=simulations,
        **kwargs,
    )
    model2 = (
        create_fair_model(
            name="Risk Type 2",
            use_tef=use_tef,
            use_vuln=use_vuln,
            simulations=simulations,
            **kwargs,
        )
        if two_model
        else None
    )

    models = [model1]
    if two_model:
        models.append(model2)

    # --- Metamodel ---
    mm = pyfair.FairMetaModel(name="Meta Model", models=models) if meta_model else None
    if mm:
        mm.calculate_all()
        models.append(mm)

    # --- Reporting ---
    fsr = pyfair.FairSimpleReport(models, currency_prefix="GBP ")
    return fsr, model1, model2, mm


def create_fair_model(name, use_tef, use_vuln, simulations, **kwargs):
    """Creates a FairModel with input data based on provided parameters."""
    model = FairModel(name=name, n_simulations=simulations)

    # Input the loss magnitude parameters
    model.input_data(
        "Loss Magnitude",
        low=kwargs.get(f"lm_low_{name[-1]}"),
        mode=kwargs.get(f"lm_mode_{name[-1]}"),
        high=kwargs.get(f"lm_high_{name[-1]}"),
    )

    # Input the frequency-related parameters based on whether TEF is used
    if use_tef:
        model.input_data(
            "Threat Event Frequency",
            low=kwargs.get(f"tef_low_{name[-1]}"),
            mode=kwargs.get(f"tef_mode_{name[-1]}"),
            high=kwargs.get(f"tef_high_{name[-1]}"),
        )
    else:
        model.input_data(
            "Contact Frequency",
            low=kwargs.get(f"contact_low_{name[-1]}"),
            mode=kwargs.get(f"contact_mode_{name[-1]}"),
            high=kwargs.get(f"contact_high_{name[-1]}"),
        )
        model.input_data(
            "Probability of Action",
            low=kwargs.get(f"action_low_{name[-1]}"),
            mode=kwargs.get(f"action_mode_{name[-1]}"),
            high=kwargs.get(f"action_high_{name[-1]}"),
        )

    # Input the vulnerability/threat-related parameters based on whether vulnerability is used
    if use_vuln:
        model.input_data(
            "Vulnerability",
            low=kwargs.get(f"vuln_low_{name[-1]}"),
            mode=kwargs.get(f"vuln_mode_{name[-1]}"),
            high=kwargs.get(f"vuln_high_{name[-1]}"),
        )
    else:
        model.input_data(
            "Threat Capability",
            low=kwargs.get(f"threat_low_{name[-1]}"),
            mode=kwargs.get(f"threat_mode_{name[-1]}"),
            high=kwargs.get(f"threat_high_{name[-1]}"),
        )
        model.input_data(
            "Control Strength",
            low=kwargs.get(f"control_low_{name[-1]}"),
            mode=kwargs.get(f"control_mode_{name[-1]}"),
            high=kwargs.get(f"control_high_{name[-1]}"),
        )

    model.calculate_all()
    return model


if __name__ == "__main__":
    st.set_page_config(
        layout="wide"
    )
    st.title("PyFair Calculator")
    st.subheader(
        "Which parameters will you be providing?",
        help="If providing Contactand Action, untick Use TEF.\n\nIf providing Threat Capability and Control (Resistance) Strength, untick Use Vulnerability",
    )
    provided1, provided2, provided3, provided4 = st.columns(spec=4)
    with provided1:
        use_tef = st.checkbox("Use TEF", value=True)
    with provided2:
        use_vuln = st.checkbox("Use Vulnerability", value=True)
    with provided3:
        two_model = st.checkbox("Use Second Model", value=False)
    with provided4:
        meta_model = st.checkbox("Generate Meta Model", value=False)

    simulations = st.slider(
        "Number of Simulations", min_value=10000, max_value=100000, step=10000
    )
    results_args = {}
    columns = []
    if not use_tef and not use_vuln:
        col1, col2, col3, col4, col5, col6 = st.columns(spec=[0.5, 1, 1, 1, 1, 1])
        columns = [col1, col2, col3, col4, col5, col6]
    elif not use_tef or not use_vuln:
        col1, col2, col3, col4, col5 = st.columns(spec=[0.5, 1, 1, 1, 1])
        columns = [col1, col2, col3, col4, col5]
    else:
        col1, col2, col3, col4 = st.columns(spec=[0.5, 1, 1, 1])
        columns = [col1, col2, col3, col4]

    no_of_models = 1 if not two_model else 2

    for model in range(1, no_of_models + 1):
        with col1:
            st.write(f"Model {model}")
            st.write("Low")
            st.write("")
            st.write("Mode")
            st.write("")
            st.write("High")
            st.write("")
        with col2:
            lm_display(model)

        with col3:
            if use_tef:
                tef_display(model)

            elif not use_tef:
                contact_display(model)

        with col4:
            if not use_tef:
                action_display(model)

        if not use_vuln:
            with columns[len(columns) - 2]:
                threat_display(model)
            with columns[len(columns) - 1]:
                control_display(model)
        else:
            with columns[-1]:
                vuln_display(model)

    submitted = st.button("Calculate")

    if submitted:
        fsr, model1, model2, mm = calculate_risk(
            simulations=simulations,
            use_tef=use_tef,
            use_vuln=use_vuln,
            two_model=two_model,
            meta_model=meta_model,
            **results_args,
        )
        if fsr:
            st.success("Model Generated")
            binary_file = fsr.to_html("output.html")
            with open("output.html", "rb") as file:
                btn = st.download_button(
                    label="Download Report",
                    data=file,
                    file_name="output.html",
                    mime="text/html",
                )
            df_model1 = model1.export_results()
            if two_model:
                df_model2 = model2.export_results()
            if meta_model:
                df_mm = mm.export_results()

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_model1.to_excel(writer, sheet_name="Model 1", index=False)
                if two_model:
                    df_model2.to_excel(writer, sheet_name="Model 2", index=False)
                if meta_model:
                    df_mm.to_excel(writer, sheet_name="Meta Model", index=False)
            output.seek(0)
            xlsx_btn = st.download_button(
                label="Download Simulation as XLSX",
                data=output,
                file_name="output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        else:
            st.error("Error generating Model")
