package main

import (
	"context"
	"flag"
	"log"
	"time"

	helloworldv1 "automation_demo/gen/helloworld/v1"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	addr := flag.String("addr", "127.0.0.1:50051", "server address")
	name := flag.String("name", "Linux", "name to greet")
	flag.Parse()

	dialCtx, dialCancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer dialCancel()

	conn, err := grpc.DialContext(
		dialCtx,
		*addr,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithBlock(),
	)
	if err != nil {
		log.Fatalf("connect to %s: %v", *addr, err)
	}
	defer conn.Close()

	client := helloworldv1.NewGreeterServiceClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	resp, err := client.SayHello(ctx, &helloworldv1.SayHelloRequest{Name: *name})
	if err != nil {
		log.Fatalf("call SayHello: %v", err)
	}

	log.Printf("response: %s", resp.GetMessage())
}
