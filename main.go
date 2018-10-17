package main

import (
	"flag"
	"fmt"
	"strings"
)

func main() {
	fpath := flag.String("path", "", "File path")
	_e_values := flag.String("e", "", "Extrimist")
	_a_values := flag.String("a", "", "Averages")
	_c_values := flag.String("c", "", "chart")
	flag.Parse()
	var app WeathermanApplication
	if *fpath != "" {
		app.Init(*fpath)
	} else {
		fmt.Println("File path is not given.")
		return
	}
	if *_e_values != "" {
		years := strings.Split(*_e_values, " ")
		for _, year := range years {
			app.ReadYearWeather(year)
			app.find_highest_lowest_temperature_and_max_humidity()
		}
	}
	if *_a_values != "" {
		year_months := strings.Split(*_a_values, " ")
		for _, year_month := range year_months {
			year_month := strings.Split(year_month, "/")
			app.ReadMonthWeather(year_month[0], year_month[1])
			app.find_average_max_temp_low_temp_and_mean_humidity()
		}
	}
	if *_c_values != "" {
		year_months := strings.Split(*_c_values, " ")
		for _, year_month := range year_months {
			year_month := strings.Split(year_month, "/")
			app.ReadMonthWeather(year_month[0], year_month[1])
			app.bar_chart_vertically()
			app.bar_chart_horizentally()
		}
	}
}
