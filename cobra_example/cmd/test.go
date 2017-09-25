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
	"context"
	"crypto/tls"
	"fmt"
	"github.com/spf13/cobra"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/clientcredentials"
	//"log"
	"net/http"
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

	/// Flag variable
	times        int
	clientId     string
	clientSecret string
	tokenUrl     string
	protectedUrl string

	oauthConfig *clientcredentials.Config
	ctx         context.Context
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
	testCmd.Flags().StringVarP(&clientId, "client_id", "c", "", "application client ID")
	testCmd.Flags().StringVarP(&clientSecret, "client_secret", "s", "", "application client Secret")
	testCmd.Flags().StringVarP(&tokenUrl, "token_url", "u", "https://phriscage-trial-test.apigee.net/oauth/v2/token", "oauth server token URL")
	testCmd.Flags().StringVarP(&protectedUrl, "protected_url", "p", "https://phriscage-trial-test.apigee.net/envirophat", "oauth server token URL")
}

// main logic
func test(cmd *cobra.Command, args []string) {
	fmt.Println("test called")
	// handle any missing args
	// max := 10
	max := 0
	switch {
	case times < max:
		fmt.Printf("%d is not greater than %d\n", times, max)
		return
	}
	fmt.Println(args)
	// this should match whatever service has given you
	// client credential access
	ctx = context.Background()
	oauthConfig = &clientcredentials.Config{
		ClientID:     clientId,
		ClientSecret: clientSecret,
		TokenURL:     tokenUrl,
		//Endpoint: oauth2.Endpoint{
		// AuthURL:  "https://oauth.example.com/dex/auth",
		//TokenURL: "https://oauth.example.com/oauth/token",
		//},
		Scopes: []string{"iot"},
	}

	// add transport for self-signed certificate to context
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}

	httpClient := &http.Client{Transport: tr}
	ctx = context.WithValue(ctx, oauth2.HTTPClient, httpClient)

	// you can modify the client (for example ignoring bad certs or otherwise)
	// by modifying the context
	client := oauthConfig.Client(ctx)

	fmt.Println(client)
	// the client will update its token if it's expired
	resp, err := client.Get(protectedUrl)
	if err != nil {
		panic(err)
	}
	fmt.Println(resp)
}
