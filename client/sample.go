package main

import (
	"context"
	"crypto/tls"
	"fmt"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/clientcredentials"
	//"log"
	"net/http"
)

var (
	//conf *oauth2.Config
	oauthConfig *clientcredentials.Config
	ctx         context.Context
)

func main() {

	// this should match whatever service has given you
	// client credential access
	ctx = context.Background()
	// conf = &oauth2.Config{
	oauthConfig = &clientcredentials.Config{
		ClientID:     "54f0c455-4d80-421f-82ca-9194df24859d",
		ClientSecret: "a0f2742f-31c7-436f-9802-b7015b8fd8e6",
		TokenURL:     "https://mag.paychex.apim.ca.com:8443/auth/oauth/v2/token",
		//Endpoint: oauth2.Endpoint{
		// AuthURL:  "https://oauth.example.com/dex/auth",
		//TokenURL: "https://mag.paychex.apim.ca.com:8443/auth/oauth/v2/token",
		//},
		Scopes: []string{"mas_storage", "oob"},
	}

	// add transport for self-signed certificate to context
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}

	sslcli := &http.Client{Transport: tr}
	ctx = context.WithValue(ctx, oauth2.HTTPClient, sslcli)

	// you can modify the client (for example ignoring bad certs or otherwise)
	// by modifying the context
	client := oauthConfig.Client(ctx)

	// the client will update its token if it's expired
	resp, err := client.Get("https://mag.paychex.apim.ca.com:8443/paychex/token/validate")
	if err != nil {
		panic(err)
	}
	fmt.Println(resp)
}
