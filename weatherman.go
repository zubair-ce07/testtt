package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
)

var READINGS [] weatherInfo

type weatherInfo struct {

	date string
	maxTemp int
	meanTemp int
	minTemp int
	maxHumidity int
	meanHumidity int
	minHumidity int
}

func ReadFileData(fileName string) []string{
	var fileData []string
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fileData = append(fileData, scanner.Text())
	}
	return fileData
}


func ParseRawData(rawData[] string) [][]string{
	var data [][]string
	for i :=0; i< len(rawData); i++{
		parsedData := strings.Split(rawData[i], ",")
		data = append(data, parsedData)
	}
	return data
}

func PopulateREADINGS(data[][] string){

	for i := 1; i < len(data); i++{
		date := data[i][0]
		maxtemp, _ := strconv.Atoi(data[i][1])
		meanTemp, _ := strconv.Atoi(data[i][2])
		minTemp, _ := strconv.Atoi(data[i][3])
		maxHumidity, _ := strconv.Atoi(data[i][7])
		meanHumidity, _ := strconv.Atoi(data[i][8])
		minHumidity, _ := strconv.Atoi(data[i][9])
		weatherData := weatherInfo{ date, maxtemp, meanTemp, minTemp,
			maxHumidity, meanHumidity, minHumidity,
		}
		READINGS = append(READINGS, weatherData)
	}
}

func ReadAllFileNames(path string) []string {
	var fileNames []string
	root := path
	err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		fileNames = append(fileNames, path)
		return nil
	})
	if err != nil {
		panic(err)
	}
	return fileNames
}

func AppendAllFilesData(fileNames[] string){

	var rawData []string
	var data [][]string
	for i := 1; i<len(fileNames); i++ {
		rawData = ReadFileData(fileNames[i])
		data = ParseRawData(rawData)
		PopulateREADINGS(data)
	}
}

func GetYearData(year string) map[string]string{

	highestTemp := 0
	lowestTemp := 50
	highestHumidity := 0
	highestTempDate := ""
	lowestTempDate := ""
	highestHumidityDate := ""
	for _, reading := range READINGS {
		if strings.Contains(reading.date , year) {
			if reading.maxTemp > highestTemp {
				highestTemp = reading.maxTemp
				highestTempDate = reading.date
			}
			if reading.minTemp < lowestTemp {
				lowestTemp = reading.minTemp
				lowestTempDate = reading.date
			}
			if reading.maxHumidity > highestHumidity{
				highestHumidity = reading.maxHumidity
				highestHumidityDate = reading.date
			}
		}
	}
	weatherData := make(map[string]string)
	weatherData["highestTemp"] = strconv.Itoa(highestTemp)
	weatherData["lowestTemp"] = strconv.Itoa(lowestTemp)
	weatherData["highestHumidity"] = strconv.Itoa(highestHumidity)
	weatherData["highestTempDate"] = highestTempDate
	weatherData["lowestTempDate"] = lowestTempDate
	weatherData["highestHumidityDate"] = highestHumidityDate
	return weatherData
}

func GetMonthYearData(monthYear string)(int, int, int){

	yearMonth := strings.Split(monthYear, "/")
	formattedYearMonth := fmt.Sprintf("%s-%s", yearMonth[0], yearMonth[1])
	cumulativeHighestTemp := 0
	cumulativeLowestTemp := 0
	cumulativeMeanHumidity := 0
	noOfDays := 0
	for _, reading := range READINGS {
		if strings.Contains(reading.date, formattedYearMonth){
			cumulativeHighestTemp = cumulativeHighestTemp + reading.maxTemp
			cumulativeLowestTemp = cumulativeLowestTemp + reading.minTemp
			cumulativeMeanHumidity = cumulativeMeanHumidity + reading.meanHumidity
			noOfDays++
		}
	}
	averageHighestTemp := cumulativeHighestTemp/noOfDays
	averageLowestTemp := cumulativeLowestTemp/noOfDays
	averageMeanHumidity := cumulativeMeanHumidity/noOfDays
	fmt.Printf("\nAverage Weather report for month %s\n",formattedYearMonth)
	return averageHighestTemp, averageLowestTemp, averageMeanHumidity
}

func GenerateExtremeReport(weatherData  map[string]string){

	fmt.Print("Extreme Weather Report")
	fmt.Printf("\nHighest: %sC on %s \n", weatherData["highestTemp"], weatherData["highestTempDate"])
	fmt.Printf("Lowest: %sC on %s \n", weatherData["lowestTemp"], weatherData["lowestTempDate"])
	fmt.Printf("Humidity: %sC on %s \n", weatherData["highestHumidity"], weatherData["highestHumidityDate"])
}

func GenerateAverageReport(averageHighestTemp int, averageLowestTemp int, averageMeanHumidity int){

	fmt.Printf("Highest Average: %sC\n", strconv.Itoa(averageHighestTemp))
	fmt.Printf("Lowest Average: %sC \n", strconv.Itoa(averageLowestTemp))
	fmt.Printf("Average Mean Humidity: %s%%\n", strconv.Itoa(averageMeanHumidity))
}

func GenerateExtremeBarChart(monthYear string) {

	yearMonth := strings.Split(monthYear, "/")
	formattedYearMonth := fmt.Sprintf("%s-%s", yearMonth[0], yearMonth[1])
	index := 1
	fmt.Printf("\n%s\n", formattedYearMonth)
	for _, reading := range READINGS {
		if strings.Contains(reading.date, formattedYearMonth) {
			highPlusSigns := strings.Repeat("+", reading.maxTemp)
			fmt.Printf("%d %s %dC \n", index, highPlusSigns, reading.maxTemp)
			lowPlusSigns := strings.Repeat("-", reading.minTemp)
			fmt.Printf("%d %s %dC \n", index, lowPlusSigns, reading.maxTemp)
			index++
		}
	}
}

func GenerateExtremeBonusChart(monthYear string) {

	yearMonth := strings.Split(monthYear, "/")
	formattedYearMonth := fmt.Sprintf("%s-%s", yearMonth[0], yearMonth[1])
	index := 1
	fmt.Printf("\n%s\n", formattedYearMonth)
	for _, reading := range READINGS {
		if strings.Contains(reading.date, formattedYearMonth) {
			highPlusSigns := strings.Repeat("+", reading.maxTemp)
			lowPlusSigns := strings.Repeat("-", reading.minTemp)
			cumulativeSigns := highPlusSigns + lowPlusSigns
			fmt.Printf("%d %s %dC %dC \n", index, cumulativeSigns, reading.maxTemp, reading.minTemp)
			index++
		}
	}
}

func GenerateReports(arguments[] string){

	path := arguments[1]
	var reports [] string
	var inputs [] string
	if len(arguments) > 3{
		reports = append(reports, arguments[2])
		inputs = append(inputs, arguments[3])
	}
	if len(arguments) > 5{
		reports = append(reports, arguments[4])
		inputs = append(inputs, arguments[5])
	}
	if len(arguments) > 7{
		reports = append(reports, arguments[6])
		inputs = append(inputs, arguments[7])
	}
	if len(arguments) > 9{
		reports = append(reports, arguments[8])
		inputs = append(inputs, arguments[9])
	}
	ValidateInput(inputs)
	fileNames := ReadAllFileNames(path)
	AppendAllFilesData(fileNames)
	for i := 0; i < len(inputs); i++ {
		switch reports[i] {
		case "-e":
			GenerateExtremeReport(GetYearData(inputs[i]))
		case "-a":
			GenerateAverageReport(GetMonthYearData(inputs[i]))
		case "-c":
			GenerateExtremeBarChart(inputs[i])
		case "-b":
			GenerateExtremeBonusChart(inputs[i])
		default:
			fmt.Println("Please input correct values")
		}
	}
}

func ValidateInput(arguments[] string){
	for i := 0; i < len(arguments); i++{
		yearMonth := strings.Split(arguments[i], "/")
		ValidateYear(yearMonth[0])
		if len(yearMonth) > 1{
			ValidateMonth(yearMonth[1])
		}
	}
}

func ValidateYear(input string){
	year, _ := strconv.Atoi(input)
	if year > 2016 || year < 2004 {
		fmt.Println("Input year is invalid")
		runtime.Breakpoint()
	}
}

func ValidateMonth(input string){
	month, _ := strconv.Atoi(input)
	if month > 12 || month < 1 {
		fmt.Println("Input month is invalid")
		runtime.Breakpoint()
	}
}

func main() {

	arguments := os.Args
	GenerateReports(arguments)
}
