// Copyright © 2017 Chris Page <phriscage@gmail.com>
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  // See the License for the specific language governing permissions and
// limitations under the License.

package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var (
	// testCmd represents the test command
	testCmd = &cobra.Command{
		Use:   "test",
		Short: "Testing the connection for OAuth",
		Long: `A longer description that spans multiple lines and likely contains examples
	and usage of using your command. For example:
	
	Cobra is a CLI library for Go that empowers applications.
	This application is a tool to generate the needed files
	to quickly create a Cobra application.`,
		//Run: func(cmd *cobra.Command, args []string) {
		//fmt.Println("test called")
		//},
		Run: test,
	}

	// alias for test
	test1Cmd = &cobra.Command{
		Hidden: true,
		Use:    "test",
		Short:  "Testing the connection for OAuth",
		Long:   ``,
		Run:    test,
	}

	/// sample Flag var
	times int
)

func init() {
	RootCmd.AddCommand(testCmd)
	RootCmd.AddCommand(test1Cmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// testCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// testCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
	testCmd.Flags().IntVarP(&times, "times", "t", 1, "times to echo the input")
}

// main logic
func test(cmd *cobra.Command, args []string) {
	fmt.Println("test called")
	// handle any missing args
	max := 10
	switch {
	case times < max:
		fmt.Printf("%d is not greater than %d\n", times, max)
		return
	}
	fmt.Println(args)
}
