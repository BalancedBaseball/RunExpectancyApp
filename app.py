from htmltools import TagList
from shiny import reactive
from shiny.express import input, render, ui
import runexpectancyfunctions as ref

ui.page_opts(
    title="Balanced Baseball Run Expectancy App",   
)

with ui.nav_panel("Evaluate Plays"):

    ui.h2("Evaluate Plays Using Run Expectancy or Run Probability")

    with ui.layout_columns(col_widths=(2, 5, 5)):
        with ui.card():

            # ui.HTML("<h4><b>Step 1: Data Details, Bases, and Outs</b></h4>")

            ui.card_header("Step 1: Data Details, Bases, and Outs", style="color:black; background:#ed7e8d !important; font-size:125%;")

            ui.input_select(  # radio buttons output a string
            "chooseyear",  
            "Choose year:",  
                {  
                    #"2024": "2024",  
                    "2023": "2023",
                    "2022": "2022",
                    "2021": "2021",
                    "2020": "2020",
                    "2019": "2019",
                    "2018": "2018",
                    "2017": "2017",
                    "2016": "2016",
                    "2015": "2015",
                },  
            )

            ui.HTML("<i><b>Note: </b>Tables for the 2024 season will be posted at the conclusion of the 2024 postseason.</i>")
                                
            ui.input_checkbox_group(  # checkbox group outputs a tuple
                "datafilter",  
                "Choose game types:",  
                {
                    "pre": "Spring Training",
                    "reg": "Regular Season",  
                    "post": "All Postseason",  
                },  
                selected = "reg"
            )

            ui.input_checkbox_group(  # checkbox group outputs a tuple
                "bases",  
                "Choose occupied bases:",  
                {  
                    "1b": "1st",  
                    "2b": "2nd",  
                    "3b": "3rd",  
                },  
            )
            
            ui.input_radio_buttons(  # radio buttons output a string
                "outs",  
                "Choose number of outs:",  
                {"0": "0", "1": "1", "2": "2"},  
            )        
    
    

        with ui.card():

            ui.card_header("Step 2: Play Selection and Probabilities", style="color:black; background:#ffe6a6 !important; font-size:125%;")

            # ui.HTML("<h4><b>Step 2: Play Selection and Probabilities</b></h4>")

            with ui.layout_columns(width = 1 / 2):
                with ui.card():
                    ui.input_select(  #select (single) outputs a string
                        "play",  
                        "Choose play:",  
                        {"noplay": "(Select)", "steal": "Steal", "bunt": "Bunt"},  
                    )

                    with ui.panel_conditional("input.play === 'steal'"):
                        ui.input_checkbox_group(  # checkbox group outputs a tuple
                        "stealrunnerdestinations",  
                        "Steal: which base(s) is the runner(s) advancing to?",  
                        {  
                            "1bstay": "Runner on 1st stays",
                            "1bto2b": "Runner on 1st advances to 2nd",
                            "2bstay": "Runner on 2nd stays",  
                            "2bto3b": "Runner on 2nd advances to 3rd",
                            "3bstay": "Runner on 3rd stays",  
                            "3bscore": "Runner on 3rd tries to score",  
                        },  
                    )
                        
                        @reactive.effect
                        @reactive.event(input.stealrunnerdestinations)
                        def stayandgo_1b():
                            if "1bstay" in input.stealrunnerdestinations() and "1bto2b" in input.stealrunnerdestinations():
                                button = ui.modal_button("OK")
                                m = ui.modal(  
                                    "Warning: The runner on first base cannot both stay and attempt to advance to second base!",  
                                    easy_close=False,  
                                    footer=button,
                                    size = "l"  
                                )
                                ui.modal_show(ui.TagList(m, button))
                                
                        @reactive.effect
                        @reactive.event(input.stealrunnerdestinations)
                        def stayandgo_2b():
                            if "2bstay" in input.stealrunnerdestinations() and "2bto3b" in input.stealrunnerdestinations():
                                button = ui.modal_button("OK")
                                m = ui.modal(  
                                    "Warning: The runner on second base cannot both stay and attempt to advance to second base!",  
                                    easy_close=False,  
                                    footer=button,
                                    size = "l"  
                                )
                                ui.modal_show(ui.TagList(m, button))

                        @reactive.effect
                        @reactive.event(input.stealrunnerdestinations)
                        def stayandgo_3b():
                            if "3bstay" in input.stealrunnerdestinations() and "3bscore" in input.stealrunnerdestinations():
                                button = ui.modal_button("OK")
                                m = ui.modal(  
                                    "Warning: The runner on third base cannot both stay and attempt to score!",  
                                    easy_close=False,  
                                    footer=button,
                                    size = "l"  
                                )
                                ui.modal_show(ui.TagList(m, button))


                    with ui.panel_conditional("input.play === 'bunt'"):
                        ui.input_checkbox_group(  # checkbox group outputs a tuple
                            "buntrunnerdestinations",  
                            "Bunt: which base(s) is the runner(s) advancing to?",  
                            {
                                "1bto2b": "Runner on 1st advances to 2nd",
                                "2bstay": "Runner on 2nd stays",  
                                "2bto3b": "Runner on 2nd advances to 3rd",
                                "3bstay": "Runner on 3rd stays",  
                                "3bscore": "Runner on 3rd tries to score",  
                            },  
                        )
                                
                        @reactive.effect
                        @reactive.event(input.buntrunnerdestinations)
                        def stayandgo_2b_bunt():
                            if "2bstay" in input.buntrunnerdestinations() and "2bto3b" in input.buntrunnerdestinations():
                                button = ui.modal_button("OK")
                                m = ui.modal(  
                                    "Warning: The runner on second base cannot both stay and attempt to advance to second base!",  
                                    easy_close=False,  
                                    footer=button,
                                    size = "l"  
                                )
                                ui.modal_show(ui.TagList(m, button))

                        @reactive.effect
                        @reactive.event(input.buntrunnerdestinations)
                        def stayandgo_3b_bunt():
                            if "3bstay" in input.buntrunnerdestinations() and "3bscore" in input.buntrunnerdestinations():
                                button = ui.modal_button("OK")
                                m = ui.modal(  
                                    "Warning: The runner on third base cannot both stay and attempt to score!",  
                                    easy_close=False,  
                                    footer=button,
                                    size = "l"  
                                )
                                ui.modal_show(ui.TagList(m, button))

                    with ui.panel_conditional("input.play != 'noplay'"):
                        ui.input_slider("one_base_error", "Enter probability of an error that allows runners (and the batter, if applicable) to advance one additional base.", 0, 100, 0)
                        # slider outputs an int
            
                with ui.card():
                    ui.h6("Enter the following probabilities:")

                    with ui.panel_conditional("input.play === 'steal'"):
                        ui.input_slider("steal_probability", "Enter probability all runner(s) steal successfully.", 0, 100, 0)
                        # slider outputs an int

                    with ui.panel_conditional("input.play === 'bunt'"):
                        ui.input_slider("bunt_probability", "Enter probability the bunt is executed successfully and the batter is out on sacrifice.", 0, 100, 0)
                        # slider outputs an int
                        
                        ui.input_slider("failed_bunt_probability", "Enter probability the batter records an out, fails to bunt, and no runners advance.", 0, 100, 0)
                        # slider outputs an int

                        ui.input_slider("bunt_for_hit_probability", "Enter probability of bunting for a hit, where the batter and every runner advances one base.", 0, 100, 0)
                        # slider outputs an int

        with ui.card():
            # ui.HTML("<h4><b>Step 3: Evaluate and Explanation</b></h4>")

            ui.card_header("Step 3: Evaluate and Explanation", style="color:black; background:#baddff !important; font-size:125%;")

            ui.input_radio_buttons(  
                "run_expectancy_or_run_probability",  
                "Evaluate by:",  
                {"RE": "Run Expectancy", "RP": "Run Probability"},  
            )  

            ui.input_action_button("apply_button", "Evaluate Play")  # action button counts number of clicks

            with ui.panel_conditional("input.apply_button === 0"):
                ui.div(ui.HTML("<b>Decision:</b> -"))
                ui.div(ui.HTML("<b>Starting Run Expectancy:</b> -"))
                ui.div(ui.HTML("<b>Aggregate Alternate Run Expectancy:</b> -"))
                ui.div(ui.HTML("<b>Explanation:</b> -"))

            @render.ui()
            @reactive.event(input.apply_button)
            def compute():
                # Collect inputs from other parts of the app
                play = input.play()
                if play == 'noplay':
                    return ui.TagList(ui.div(ui.HTML("<b>Error: </b> Please choose a play to evaluate!")))
                if play == 'steal':
                    runner_destinations, warning = ref.runner_destinations_to_digits(input.stealrunnerdestinations())
                    if warning != '':
                        return ui.TagList(ui.div(ui.HTML("<b>Error: </b>" + warning)))
                    steal_probability = input.steal_probability()
                    bunt_probability = 0
                    failed_bunt_probability = 0
                    bunt_for_hit_probability = 0
                    one_base_error_probability = input.one_base_error()
                if play == 'bunt':
                    runner_destinations, warning = ref.runner_destinations_to_digits(input.buntrunnerdestinations())
                    if warning != '':
                        return ui.TagList(ui.div(ui.HTML("<b>Error: </b>" + warning)))
                    steal_probability = 0
                    bunt_probability = input.bunt_probability()
                    failed_bunt_probability = input.failed_bunt_probability()
                    bunt_for_hit_probability = input.bunt_for_hit_probability()
                    one_base_error_probability = input.one_base_error()
                probabilities = steal_probability + bunt_probability + failed_bunt_probability + bunt_for_hit_probability + one_base_error_probability
                if probabilities > 100:
                    return ui.TagList(ui.div(ui.HTML("<b>Error: </b>All probabilities on this play must be no greater than 100!")))
                year = int(input.chooseyear())
                gametypes = ''.join(input.datafilter())
                if gametypes == '':
                    return ui.TagList(ui.div(ui.HTML("<b>Error: </b>Please choose at least one of Spring Training, Regular Season, or Postseason!")))
                if runner_destinations == '000':
                    return ui.TagList(ui.div(ui.HTML("<b>Error: </b>Runner destinations cannot be empty!")))
                if ref.all_runners_stay(runner_destinations):
                    return ui.TagList(ui.div(ui.HTML("<b>Error: </b>At least one runner must attempt to advance a base!")))
                bases_occupied = ref.bases_to_bases_occupied(input.bases())
                if bases_occupied == '000':
                    return ui.TagList(ui.div(ui.HTML("<b>Error: </b>Bases occupied cannot be empty!")))
                if not ref.check_bases_occupied_and_runner_destinations(bases_occupied, runner_destinations):
                    return ui.TagList(ui.div(ui.HTML("<b>Error: </b>Bases occupied and runner destinations do not match!")))
                outs = input.outs()
                if play == 'bunt' and bunt_for_hit_probability > 0:
                    bunt_hit = True
                else:
                    bunt_hit = False
                if play == 'bunt' and failed_bunt_probability > 0:
                    failed_bunt = True
                else:
                    failed_bunt = False
                if one_base_error_probability > 0:
                    one_base_error = True
                else:
                    one_base_error = False

                # Run the functions
                if input.run_expectancy_or_run_probability() == 'RE':
                    REandRuns = ref.evaluate_play_RE(play, runner_destinations, year, gametypes, bases_occupied, outs, bunt_hit, failed_bunt, one_base_error)
                    decision, starting_effective_RE, alt_effective_RE, explanation = ref.make_decision_RE_and_explain(play, REandRuns, bunt_probability, steal_probability, bunt_for_hit_probability, failed_bunt_probability, one_base_error_probability)
                if input.run_expectancy_or_run_probability() == 'RP':
                    RPandRuns = ref.evaluate_play_RP(play, runner_destinations, year, gametypes, bases_occupied, outs, bunt_hit, failed_bunt, one_base_error)
                    decision, starting_effective_RP, alt_effective_RP, explanation = ref.make_decision_RP_and_explain(play, RPandRuns, bunt_probability, steal_probability, bunt_for_hit_probability, failed_bunt_probability, one_base_error_probability)


                # Display outputs
                ## Display decision and/or graphic
                decision = ui.div(ui.HTML("<b>Decision: </b>"), decision)

                ## Show comparison RE values
                if input.run_expectancy_or_run_probability() == 'RE':
                    starting_effective_RE_rounded = round(starting_effective_RE, 2)
                    start_RE = ui.div(ui.HTML("<b>Starting Run Expectancy: </b>"), starting_effective_RE_rounded)
                    alternative_effective_RE_rounded = round(alt_effective_RE, 2)
                    end_RE = ui.div(ui.HTML("<b>Aggregate Alternative Run Expectancy: </b>"), alternative_effective_RE_rounded)

                ## Format explanation as text
                    explanation = ui.div(ui.HTML("<b>Explanation: </b>"), explanation)
                    return ui.TagList(decision, start_RE, end_RE, explanation)
                
                ## Show comparison RE values
                if input.run_expectancy_or_run_probability() == 'RP':
                    starting_effective_RP_rounded = round(starting_effective_RP, 2)
                    start_RP = ui.div(ui.HTML("<b>Starting Run Probability: </b>"), starting_effective_RP_rounded, "%")
                    alternative_effective_RP_rounded = round(alt_effective_RP, 2)
                    end_RP = ui.div(ui.HTML("<b>Aggregate Alternative Run Probability: </b>"), alternative_effective_RP_rounded, "%")

                ## Format explanation as text
                    explanation = ui.div(ui.HTML("<b>Explanation: </b>"), explanation)
                    return ui.TagList(decision, start_RP, end_RP, explanation)

with ui.nav_panel("View Tables"):
    ui.h2("Run Expectancy & Run Probability Tables")

    with ui.layout_columns(col_widths=(6, 6)):
        with ui.card():
            with ui.layout_column_wrap(width=1 / 2):
                with ui.card():
                    ui.input_select(  # radio buttons output a string
                            "chooseyear3",  
                            "Choose year:",  
                                {  
                                #"2024": "2024",  
                                "2023": "2023",
                                "2022": "2022",
                                "2021": "2021",
                                "2020": "2020",
                                "2019": "2019",
                                "2018": "2018",
                                "2017": "2017",
                                "2016": "2016",
                                "2015": "2015",
                                },
                        )
                    
                    ui.HTML("<i><b>Note: </b>Tables for the 2024 season will be posted at the conclusion of the 2024 postseason.</i>")
                
                with ui.card():
                    ui.input_checkbox_group(  # checkbox group outputs a tuple
                            "datafilter3",  
                            "Choose game types:",  
                            {
                                "pre": "Spring Training",
                                "reg": "Regular Season",
                                "post": "All Postseason",  
                            },  
                            selected = "reg"
                        )
                    
                    ui.input_radio_buttons(  
                        "run_expectancy_or_run_probability3",  
                        "View:",  
                        {"RE": "Run Expectancy Table", "RP": "Run Probability Table"},  
                    )
                    
                    ui.input_action_button("apply_button3", "View Table")  # action button counts number of clicks
        
        with ui.card():

            ui.div(ui.HTML("For information on reading Run Expectancy or Run Probability Tables, see the \"Tutorial Videos and About\" tab."))
                
            @render.ui
            @reactive.event(input.apply_button3)
            def show_table_text3():
                if input.run_expectancy_or_run_probability3() == 'RE':
                    title = ui.div(ui.h4("Run Expectancy Table"))
                if input.run_expectancy_or_run_probability3() == 'RP':
                    title = ui.div(ui.h4("Run Probability Table"))
                return TagList(title)

            @render.data_frame
            @reactive.event(input.apply_button3)  
            def show_table3():
                import pandas as pd
                year = int(input.chooseyear3())
                gametypes = ''.join(input.datafilter3())
                if input.run_expectancy_or_run_probability3() == 'RE':
                    df = pd.read_csv(f'RE24_{year}_{gametypes}.csv')
                    df = df.set_index("Bases")
                    df = df.reindex(index=[0, 100, 10, 1, 110, 101, 11, 111])
                    df = df.rename({0: "Empty", 1: "Runner on 3rd",
                        10: "Runner on 2nd", 100: "Runner on 1st",
                        11: "2nd and 3rd", 101: "1st and 3rd",
                        110: "1st and 2nd", 111: "Bases Loaded"})
                    df = df.reset_index()
                    df = df.rename(columns = {"Bases": "Bases \ Outs"})
                    table = render.DataGrid(df)
                    return table
                if input.run_expectancy_or_run_probability3() == 'RP':
                    df = pd.read_csv(f'RP24_{year}_{gametypes}.csv')
                    df = df.set_index("Bases")
                    df = df.reindex(index=[0, 100, 10, 1, 110, 101, 11, 111])
                    df = df.rename({0: "Empty", 1: "Runner on 3rd",
                        10: "Runner on 2nd", 100: "Runner on 1st",
                        11: "2nd and 3rd", 101: "1st and 3rd",
                        110: "1st and 2nd", 111: "Bases Loaded"})
                    df = df.reset_index()
                    df = df.rename(columns = {"Bases": "Bases \ Outs"})
                    table = render.DataGrid(df)
                    return table
            
with ui.nav_panel("Tutorial Videos and About"):
    with ui.layout_columns(col_widths=(-2, 8, -2)):
        with ui.card():
            ui.h2("About this App")

            ui.div("Thank you for visiting the Balanced Baseball Run Expectancy App!")

            ui.div(ui.HTML("<b>How to Read a Run Expectancy Table:</b> The left-most column indicates which bases have runners, while the top row indicates how many outs are in the inning. To find your bases-outs scenario, find the column with the number of outs, then find the row with the bases occupied. The run expectancy value at the corresponding position in the table represents the average number of runs teams scored in an inning during or after that plate appearance. So a run expectancy of 0.79 means teams scored an average of 0.79 runs during or after reaching this bases-outs combination. For more information on run expectancy, see <a href=\"https://library.fangraphs.com/misc/re24/\">this FanGraphs article.</a>"))

            ui.div(ui.HTML("<b>Run Probability:</b> I have made basic modifications to the Run Expectancy script in order to compute the percentage of plate appearances in a given scenario in which at least one or more runs are scored later in the inning. Note that this may include the runners on-base, the batter at the plate, or even a later batter or runner who may reach base. So a run probability of 0.59 means teams scored in 59% of plate appearances during or after reaching this bases-outs combination."))

            ui.div(ui.HTML("<b>How the app makes decisions:</b> Using statcast data for all available Major League Baseball seasons, we are able to compute run expectancy tables for each season. We can use this data to decide whether certain baseball moves, like a bunt or steal, are risks worth taking in the current run-scoring environment. As you may be aware, every season brings different levels of offense in Major League Baseball. This app allows you to enter any scenarios to decide whether a certain move increases or decreases the offensive team's run expectancy."))

            ui.div(ui.HTML("<b>Aggregate alternative run expectancy:</b> The app looks at the starting run expectancy of the scenario. This number is compared to a weighted average of run expectancies based on the user's entered probabilities for each alternative event. The app subtracts the probabilities of those events from 1 to obtain the probability of failure, where for simplicity, we assume that the lead runner on the bunt or steal is thrown out. Other scenarios are detailed based on the user's input. Based on which of the starting or alternative run expectancies are larger, the app makes a decision on the move with an explanation."))

        with ui.card():
            ui.h2("Tutorial Videos")

            ui.div("How to Use this App")

            ui.div("Walkthrough on Computing Run Expectancy in Python")

            ui.div("Investigating Basic Baseball Questions with Run Expectancy in Python")

            ui.div(ui.HTML("GitHub code: <a href='https://github.com/BalancedBaseball/RunExpectancyApp'> https://github.com/BalancedBaseball/RunExpectancyApp</a>"))

with ui.nav_panel("Further Reading/Learning"):
    with ui.layout_columns(col_widths=(-2, 8, -2)):
        with ui.card():
            ui.HTML("<div><i>Analyzing Baseball Data with R, 3rd Edition</i> by Jim Albert, Benjamin S. Baumer, and Max Marchi</div>")

            ui.div("Run Expectancy Explained by Simple Sabermetrics")

            ui.div("My website: Balanced Baseball")
