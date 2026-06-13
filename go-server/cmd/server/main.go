package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"

	helloworldv1 "automation_demo/gen/helloworld/v1"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

type greeterServer struct {
	helloworldv1.UnimplementedGreeterServiceServer
}

func (s *greeterServer) SayHello(ctx context.Context, req *helloworldv1.SayHelloRequest) (*helloworldv1.SayHelloResponse, error) {
	name := req.GetName()
	if name == "" {
		name = "gRPC"
	}

	return &helloworldv1.SayHelloResponse{
		Message: fmt.Sprintf("Hello, %s!", name),
	}, nil
}

func main() {
	addr := flag.String("addr", ":50051", "server listen address")
	flag.Parse()

	listener, err := net.Listen("tcp", *addr)
	if err != nil {
		log.Fatalf("listen on %s: %v", *addr, err)
	}

	server := grpc.NewServer()
	helloworldv1.RegisterGreeterServiceServer(server, &greeterServer{})
	reflection.Register(server)

	log.Printf("gRPC server listening on %s", *addr)
	if err := server.Serve(listener); err != nil {
		log.Fatalf("serve grpc: %v", err)
	}
}
