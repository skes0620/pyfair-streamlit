import pyfair
from pyfair import FairModel
import warnings
import streamlit as st
from decimal import Decimal
import pandas as pd
from io import BytesIO

warnings.simplefilter(action="ignore", category=FutureWarning)


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
    col1, col2, col3, col4 = st.columns(spec=4)
    with col1:
        st.write("Model 1 - Input Type")
        st.write("Loss Magnitude (£ million)")
        if use_tef:
            st.write("TEF (per year)")
            st.write("")
        else:
            st.write("Contact Frequency (per year)")
            st.write("Probability of Action (%)")
        if use_vuln:
            st.write("Vulnerability (% per year)")
        else:
            st.write("Threat Capacity (%)")
            st.write("")
            st.write("Control (Resistance) Strength (%)")
            st.write("")
    with col2:
        st.write("Low")
        lm_low_1 = float(
            Decimal(
                st.number_input(
                    label="LM LOW 1",
                    label_visibility="collapsed",
                    step=0.1,
                    min_value=0.0,
                    max_value=None,
                    value=0.1,
                )
            )
            * Decimal(1000000.00)
        )
        results_args["lm_low_1"] = lm_low_1

        if use_tef:
            tef_low_1 = st.number_input(
                label="TEF LOW 1",
                label_visibility="collapsed",
                step=1,
                min_value=0,
                max_value=None,
                value=0,
            )
            results_args["tef_low_1"] = tef_low_1

        else:
            contact_low_1 = st.number_input(
                label="Contact LOW 1",
                label_visibility="collapsed",
                step=1,
                min_value=0,
                max_value=None,
                value=2,
            )
            action_low_1 = st.number_input(
                label="Action LOW 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.00,
            )
            results_args["contact_low_1"] = contact_low_1
            results_args["action_low_1"] = action_low_1

        if use_vuln:
            vuln_low_1 = st.number_input(
                label="VULN LOW 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.0,
                max_value=1.0,
                value=0.01,
            )
            results_args["vuln_low_1"] = vuln_low_1

        else:
            threat_low_1 = st.number_input(
                label="threat LOW 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.50,
            )
            control_low_1 = st.number_input(
                label="control LOW 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.75,
            )
            results_args["threat_low_1"] = threat_low_1
            results_args["control_low_1"] = control_low_1

    with col3:
        st.write("Mode")
        lm_mode_1 = float(
            Decimal(
                st.number_input(
                    label="LM MODE 1",
                    label_visibility="collapsed",
                    step=0.1,
                    min_value=0.0,
                    max_value=None,
                    value=0.5,
                )
            )
            * Decimal(1000000.00)
        )
        results_args["lm_mode_1"] = lm_mode_1

        if use_tef:
            tef_mode_1 = st.number_input(
                label="TEF MODE 1",
                label_visibility="collapsed",
                step=1,
                min_value=0,
                max_value=None,
                value=2,
            )
            results_args["tef_mode_1"] = tef_mode_1

        else:
            contact_mode_1 = st.number_input(
                label="Contact mode 1",
                label_visibility="collapsed",
                step=1,
                min_value=0,
                max_value=None,
                value=5,
            )
            action_mode_1 = st.number_input(
                label="Action mode 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.15,
            )
            results_args["contact_mode_1"] = contact_mode_1
            results_args["action_mode_1"] = action_mode_1

        if use_vuln:
            vuln_mode_1 = st.number_input(
                label="VULN MODE 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.0,
                max_value=1.0,
                value=0.3,
            )
            results_args["vuln_mode_1"] = vuln_mode_1

        else:
            threat_mode_1 = st.number_input(
                label="threat mode 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.70,
            )
            control_mode_1 = st.number_input(
                label="control mode 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.80,
            )
            results_args["threat_mode_1"] = threat_mode_1
            results_args["control_mode_1"] = control_mode_1

    with col4:
        st.write("High")
        lm_high_1 = float(
            Decimal(
                st.number_input(
                    label="LM HIGH 1",
                    label_visibility="collapsed",
                    step=0.1,
                    min_value=0.0,
                    max_value=None,
                    value=1.0,
                )
            )
            * Decimal(1000000.00)
        )
        results_args["lm_high_1"] = lm_high_1

        if use_tef:
            tef_high_1 = st.number_input(
                label="TEF HIGH 1",
                label_visibility="collapsed",
                step=1,
                min_value=0,
                max_value=None,
                value=12,
            )
            results_args["tef_high_1"] = tef_high_1

        else:
            contact_high_1 = st.number_input(
                label="Contact high 1",
                label_visibility="collapsed",
                step=1,
                min_value=0,
                max_value=None,
                value=20,
            )
            action_high_1 = st.number_input(
                label="Action high 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.20,
            )
            results_args["contact_high_1"] = contact_high_1
            results_args["action_high_1"] = action_high_1

        if use_vuln:
            vuln_high_1 = st.number_input(
                label="VULN HIGH 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.0,
                max_value=1.0,
                value=0.5,
            )
            results_args["vuln_high_1"] = vuln_high_1

        else:
            threat_high_1 = st.number_input(
                label="threat high 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.90,
            )
            control_high_1 = st.number_input(
                label="control high 1",
                label_visibility="collapsed",
                step=0.01,
                min_value=0.00,
                max_value=1.00,
                value=0.90,
            )
            results_args["threat_high_1"] = threat_high_1
            results_args["control_high_1"] = control_high_1

    # Model 2
    if two_model:
        col1, col2, col3, col4 = st.columns(spec=4)
        with col1:
            st.write("Model 2 - Input Type")
            st.write("Loss Magnitude (£ million)")
            if use_tef:
                st.write("TEF (per year)")
                st.write("")
            else:
                st.write("Contact Frequency (per year)")
                st.write("Probability of Action (%)")
            if use_vuln:
                st.write("Vulnerability (% per year)")
            else:
                st.write("Threat Capacity (%)")
                st.write("")
                st.write("Control (Resistance) Strength (%)")
                st.write("")
        with col2:
            st.write("Low")
            lm_low_2 = float(
                Decimal(
                    st.number_input(
                        label="LM LOW 2",
                        label_visibility="collapsed",
                        step=0.1,
                        min_value=0.0,
                        max_value=None,
                        value=0.1,
                    )
                )
                * Decimal(1000000.00)
            )
            results_args["lm_low_2"] = lm_low_2

            if use_tef:
                tef_low_2 = st.number_input(
                    label="TEF LOW 2",
                    label_visibility="collapsed",
                    step=1,
                    min_value=0,
                    max_value=None,
                    value=0,
                )
                results_args["tef_low_2"] = tef_low_2

            else:
                contact_low_2 = st.number_input(
                    label="Contact low 2",
                    label_visibility="collapsed",
                    step=1,
                    min_value=0,
                    max_value=None,
                    value=2,
                )
                action_low_2 = st.number_input(
                    label="Action low 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.00,
                )
                results_args["contact_low_2"] = contact_low_2
                results_args["action_low_2"] = action_low_2

            if use_vuln:
                vuln_low_2 = st.number_input(
                    label="VULN LOW 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.0,
                    max_value=1.0,
                    value=0.01,
                )
                results_args["vuln_low_2"] = vuln_low_2

            else:
                threat_low_2 = st.number_input(
                    label="threat LOW 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.50,
                )
                control_low_2 = st.number_input(
                    label="control LOW 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.75,
                )
                results_args["threat_low_2"] = threat_low_2
                results_args["control_low_2"] = control_low_2

        with col3:
            st.write("Mode")
            lm_mode_2 = float(
                Decimal(
                    st.number_input(
                        label="LM MODE 2",
                        label_visibility="collapsed",
                        step=0.1,
                        min_value=0.0,
                        max_value=None,
                        value=0.5,
                    )
                )
                * Decimal(1000000.00)
            )
            results_args["lm_mode_2"] = lm_mode_2

            if use_tef:
                tef_mode_2 = st.number_input(
                    label="TEF MODE 2",
                    label_visibility="collapsed",
                    step=1,
                    min_value=0,
                    max_value=None,
                    value=2,
                )
                results_args["tef_mode_2"] = tef_mode_2

            else:
                contact_mode_2 = st.number_input(
                    label="Contact mode 2",
                    label_visibility="collapsed",
                    step=1,
                    min_value=0,
                    max_value=None,
                    value=5,
                )
                action_mode_2 = st.number_input(
                    label="Action mode 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.15,
                )
                results_args["contact_mode_2"] = contact_mode_2
                results_args["action_mode_2"] = action_mode_2

            if use_vuln:
                vuln_mode_2 = st.number_input(
                    label="VULN MODE 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.0,
                    max_value=1.0,
                    value=0.3,
                )
                results_args["vuln_mode_2"] = vuln_mode_2

            else:
                threat_mode_2 = st.number_input(
                    label="threat mode 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.70,
                )
                control_mode_2 = st.number_input(
                    label="control mode 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.80,
                )
                results_args["threat_mode_2"] = threat_mode_2
                results_args["control_mode_2"] = control_mode_2

        with col4:
            st.write("High")
            lm_high_2 = float(
                Decimal(
                    st.number_input(
                        label="LM HIGH 2",
                        label_visibility="collapsed",
                        step=0.1,
                        min_value=0.0,
                        max_value=None,
                        value=1.0,
                    )
                )
                * Decimal(1000000.00)
            )
            results_args["lm_high_2"] = lm_high_2

            if use_tef:
                tef_high_2 = st.number_input(
                    label="TEF HIGH 2",
                    label_visibility="collapsed",
                    step=1,
                    min_value=0,
                    max_value=None,
                    value=12,
                )
                results_args["tef_high_2"] = tef_high_2

            else:
                contact_high_2 = st.number_input(
                    label="Contact high 2",
                    label_visibility="collapsed",
                    step=1,
                    min_value=0,
                    max_value=None,
                    value=20,
                )
                action_high_2 = st.number_input(
                    label="Action high 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.20,
                )
                results_args["contact_high_2"] = contact_high_2
                results_args["action_high_2"] = action_high_2

            if use_vuln:
                vuln_high_2 = st.number_input(
                    label="VULN HIGH 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.0,
                    max_value=1.0,
                    value=0.5,
                )
                results_args["vuln_high_2"] = vuln_high_2

            else:
                threat_high_2 = st.number_input(
                    label="threat high 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.90,
                )
                control_high_2 = st.number_input(
                    label="control high 2",
                    label_visibility="collapsed",
                    step=0.01,
                    min_value=0.00,
                    max_value=1.00,
                    value=0.90,
                )
                results_args["threat_high_2"] = threat_high_2
                results_args["control_high_2"] = control_high_2

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
            df_model2 = model2.export_results()
            df_mm = mm.export_results()

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_model1.to_excel(writer, sheet_name="Model 1", index=False)
                df_model2.to_excel(writer, sheet_name="Model 2", index=False)
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
