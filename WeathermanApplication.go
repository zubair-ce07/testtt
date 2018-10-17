package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
	"time"
)

var MONTHS = [...]string{"jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"}

type weather_data_map_list [][]map[string]string

type WeathermanApplication struct {
	path              string
	weather_data_list weather_data_map_list
}

func (context *WeathermanApplication) Init(fpath string) {
	context.path = fpath
}

func (context *WeathermanApplication) ReadYearWeather(year string) {
	context.weather_data_list = [][]map[string]string{}
	for i := 0; i < 12; i++ {
		filepath := context.path + "/Murree_weather_" + year + "_" + MONTHS[i] + ".txt"
		file, err := os.Open(filepath)
		if err == nil {
			file_reader := csv.NewReader(file)
			file_reader.Comma = ','
			var header []string
			var new_month = []map[string]string{}
			for {
				record, err := file_reader.Read()
				if err == io.EOF {
					break
				}
				if err != nil {
					log.Fatal(err)
				}
				if header == nil {
					header = record
				} else {
					weather_data := map[string]string{}
					for i := range header {
						weather_data[header[i]] = record[i]
					}
					new_month = append(new_month, weather_data)
				}
			}
			context.weather_data_list = append(context.weather_data_list, new_month)
		}
	}
}

func (context *WeathermanApplication) ReadMonthWeather(year, month string) {
	context.weather_data_list = [][]map[string]string{}
	mon, _ := strconv.Atoi(month)
	filepath := context.path + "/Murree_weather_" + year + "_" + MONTHS[mon-1] + ".txt"
	file, err := os.Open(filepath)
	if err == nil {
		file_reader := csv.NewReader(file)
		file_reader.Comma = ','
		var header []string
		var new_month = []map[string]string{}
		for {
			record, err := file_reader.Read()
			if err == io.EOF {
				break
			}
			if err != nil {
				log.Fatal(err)
			}
			if header == nil {
				header = record
			} else {
				weather_data := map[string]string{}
				for i := range header {
					weather_data[header[i]] = record[i]
				}
				new_month = append(new_month, weather_data)
			}
		}
		context.weather_data_list = append(context.weather_data_list, new_month)
	}
}

func (context *WeathermanApplication) find_highest_lowest_temperature_and_max_humidity() {
	if len(context.weather_data_list) == 0 {
		fmt.Println("No Data is Available")
	} else {
		max_tempC := -999 //non real max value
		max_tempC_date := time.Now()
		min_tempC := 999
		min_tempC_date := time.Now()
		max_humidity := -999
		max_humidity_date := time.Now()
		for _, months := range context.weather_data_list {
			for _, day_weather := range months {
				layout := "2006-1-2"
				temp, err := strconv.Atoi(day_weather["Max TemperatureC"])
				if err == nil {
					if temp > max_tempC {
						max_tempC = temp
						max_tempC_date, _ = time.Parse(layout, day_weather["PKT"])
					}
				}
				temp, err = strconv.Atoi(day_weather["Min TemperatureC"])
				if err == nil {
					if temp < min_tempC {
						min_tempC = temp
						min_tempC_date, _ = time.Parse(layout, day_weather["PKT"])
					}
				}
				temp, err = strconv.Atoi(day_weather["Max Humidity"])
				if err == nil {
					if temp > max_humidity {
						max_humidity = temp
						max_humidity_date, _ = time.Parse(layout, day_weather["PKT"])
					}
				}
			}
		}
		fmt.Printf("Highest : %vC on %v %v", max_tempC, max_tempC_date.Month(), max_tempC_date.Day())
		fmt.Println()
		fmt.Printf("Lowest : %vC on %v %v", min_tempC, min_tempC_date.Month(), min_tempC_date.Day())
		fmt.Println()
		fmt.Printf("humidity : %vC on %v %v", max_humidity, max_humidity_date.Month(), max_humidity_date.Day())
		fmt.Println()
	}
}

func (context *WeathermanApplication) find_average_max_temp_low_temp_and_mean_humidity() {
	if len(context.weather_data_list) == 0 {
		fmt.Println("No Data is Available")
	} else {
		max_tempC_day_counter := 0
		min_tempC_day_counter := 0
		mean_humidity_day_counter := 0
		max_tempC_sum := 0
		min_tempC_sum := 0
		mean_humidity_sum := 0
		for _, day_weather := range context.weather_data_list[0] {
			temp, err := strconv.Atoi(day_weather["Max TemperatureC"])
			if err == nil {
				max_tempC_day_counter++
				max_tempC_sum += temp
			}
			temp, err = strconv.Atoi(day_weather["Min TemperatureC"])
			if err == nil {
				min_tempC_day_counter++
				min_tempC_sum += temp
			}
			temp, err = strconv.Atoi(day_weather[" Mean Humidity"])
			if err == nil {
				mean_humidity_day_counter++
				mean_humidity_sum += temp
			}
		}
		fmt.Printf("Highest Average : %vC", max_tempC_sum/max_tempC_day_counter)
		fmt.Println()
		fmt.Printf("Lowest Average : %vC", min_tempC_sum/min_tempC_day_counter)
		fmt.Println()
		fmt.Printf("Mean Humidity Average : %vC", mean_humidity_sum/mean_humidity_day_counter)
		fmt.Println()
	}
}

func (context *WeathermanApplication) bar_chart_vertically() {
	if len(context.weather_data_list) == 0 {
		fmt.Println("No Data is Available")
	} else {
		counter := 1
		for _, day_weather := range context.weather_data_list[0] {
			max_temp, err1 := strconv.Atoi(day_weather["Max TemperatureC"])
			min_tempC, err2 := strconv.Atoi(day_weather["Min TemperatureC"])
			if max_temp < 0 {
				max_temp *= -1
			}
			if min_tempC < 0 {
				min_tempC *= -1
			}
			if err1 == nil {
				plus := ""
				for i := 0; i < max_temp; i++ {
					plus += "+"
				}
				fmt.Println("\x1b[3;31m ", counter, plus, max_temp, "C \x1b[0m")
			}
			if err2 == nil {
				plus := "+"
				for i := 0; i < min_tempC; i++ {
					plus += "+"
				}
				fmt.Println("\x1b[3;34m ", counter, plus, min_tempC, "C \x1b[0m")
			}
			counter++
		}
	}
}

func (context *WeathermanApplication) bar_chart_horizentally() {
	if len(context.weather_data_list) == 0 {
		fmt.Println("No Data is Available")
	} else {
		counter := 1
		for _, day_weather := range context.weather_data_list[0] {
			max_tempC, err1 := strconv.Atoi(day_weather["Max TemperatureC"])
			min_tempC, err2 := strconv.Atoi(day_weather["Min TemperatureC"])
			if max_tempC < 0 {
				max_tempC *= -1
			}
			if min_tempC < 0 {
				min_tempC *= -1
			}
			if err1 == nil && err2 == nil {
				max_plus := ""
				for i := 0; i < max_tempC; i++ {
					max_plus += "+"
				}
				min_plus := ""
				for i := 0; i < min_tempC; i++ {
					min_plus += "+"
				}
				fmt.Println("\x1b[3;34m ", counter, min_plus, "\x1b[3;31m ", max_plus, min_tempC, "-", max_tempC, "C \x1b[0m")
			}
			counter++
		}
	}
}
