import pyfair
from pyfair import FairModel
import warnings
import streamlit as st
from decimal import Decimal

warnings.simplefilter(action="ignore", category=FutureWarning)


def risk_threat_1(
    simulations: int,
    use_tef: bool,
    use_vuln: bool,
    two_model: bool,
    meta_model: bool,
    **kwargs
):
    # Model 1
    model1 = FairModel(name="Risk Type 1", n_simulations=simulations)
    model1.input_data(
        "Loss Magnitude",
        low=kwargs.get("lm_low_1"),
        mode=kwargs.get("lm_mode_1"),
        high=kwargs.get("lm_high_1"),
    )
    if use_tef:
        model1.input_data(
            "Threat Event Frequency",
            low=kwargs.get("tef_low_1"),
            mode=kwargs.get("tef_mode_1"),
            high=kwargs.get("tef_high_1"),
        )
    else:
        model1.input_data(
            "Contact Frequency",
            low=kwargs.get("contact_low_1"),
            mode=kwargs.get("contact_mode_1"),
            high=kwargs.get("contact_high_1"),
        )
        model1.input_data(
            "Probability of Action",
            low=kwargs.get("action_low_1"),
            mode=kwargs.get("action_mode_1"),
            high=kwargs.get("action_high_1"),
        )
    if use_vuln:
        model1.input_data(
            "Vulnerability",
            low=kwargs.get("vuln_low_1"),
            mode=kwargs.get("vuln_mode_1"),
            high=kwargs.get("vuln_high_1"),
        )
    else:
        model1.input_data(
            "Threat Capability",
            low=kwargs.get("threat_low_1"),
            mode=kwargs.get("threat_mode_1"),
            high=kwargs.get("threat_high_1"),
        )
        model1.input_data(
            "Control Strength",
            low=kwargs.get("control_low_1"),
            mode=kwargs.get("control_mode_1"),
            high=kwargs.get("control_high_1"),
        )
    model1.calculate_all()

    # Model 2 (Identical to Model 1 for this example)
    model2 = None
    if two_model:
        model2 = FairModel(name="Risk Type 2", n_simulations=simulations)
        model2.input_data(
            "Loss Magnitude",
            low=kwargs.get("lm_low_2"),
            mode=kwargs.get("lm_mode_2"),
            high=kwargs.get("lm_high_2"),
        )
        if use_tef:
            model2.input_data(
                "Threat Event Frequency",
                low=kwargs.get("tef_low_2"),
                mode=kwargs.get("tef_mode_2"),
                high=kwargs.get("tef_high_2"),
            )
        else:
            model2.input_data(
                "Contact Frequency",
                low=kwargs.get("contact_low_2"),
                mode=kwargs.get("contact_mode_2"),
                high=kwargs.get("contact_high_2"),
            )
            model2.input_data(
                "Probability of Action",
                low=kwargs.get("action_low_2"),
                mode=kwargs.get("action_mode_2"),
                high=kwargs.get("action_high_2"),
            )
        if use_vuln:
            model2.input_data(
                "Vulnerability",
                low=kwargs.get("vuln_low_2"),
                mode=kwargs.get("vuln_mode_2"),
                high=kwargs.get("vuln_high_2"),
            )
        else:
            model2.input_data(
                "Threat Capability",
                low=kwargs.get("threat_low_2"),
                mode=kwargs.get("threat_mode_2"),
                high=kwargs.get("threat_high_2"),
            )
            model2.input_data(
                "Control Strength",
                low=kwargs.get("control_low_2"),
                mode=kwargs.get("control_mode_2"),
                high=kwargs.get("control_high_2"),
            )
        model2.calculate_all()

    models = [model1]
    if two_model:
        models.append(model2)

    # Metamodel
    mm = None
    if meta_model:
        mm = pyfair.FairMetaModel(name="Meta Model", models=models)
        mm.calculate_all()
        models.append(mm)

    # Create and Customize Report
    fsr = pyfair.FairSimpleReport(models, currency_prefix="GBP ")
    return fsr, model1, model2, mm


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
        fsr, model1, model2, mm = risk_threat_1(
            simulations=simulations,
            use_tef=use_tef,
            use_vuln=use_vuln,
            two_model=two_model,
            meta_model=meta_model,
            **results_args
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
            df = model1.export_results()
            binary_csv_file = df.to_csv("output.csv")
            with open("output.csv", "rb") as file:
                csv_btn = st.download_button(
                    label="Download Simulation as CSV",
                    data=file,
                    file_name="output.csv",
                    mime="text/csv",
                )
        else:
            st.error("Error generating Model")
