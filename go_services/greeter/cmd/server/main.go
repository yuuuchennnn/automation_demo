package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"time"

	helloworldv1 "automation_demo/gen/helloworld/v1"

	"github.com/golang/glog"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

type greeterServer struct {
	helloworldv1.UnimplementedGreeterServiceServer
}

func logUnaryRPC(
	ctx context.Context,
	req any,
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (any, error) {
	start := time.Now()
	resp, err := handler(ctx, req)
	glog.Infof("grpc request handled: method=%s duration=%s error=%v", info.FullMethod, time.Since(start), err)
	return resp, err
}

func (s *greeterServer) SayHello(ctx context.Context, req *helloworldv1.SayHelloRequest) (*helloworldv1.SayHelloResponse, error) {
	name := req.GetName()
	if name == "" {
		name = "gRPC"
	}

	message := fmt.Sprintf("Hello, %s!", name)
	glog.Infof("SayHello request received: name=%q response=%q", name, message)

	return &helloworldv1.SayHelloResponse{
		Message: message,
	}, nil
}

func main() {
	addr := flag.String("addr", ":50051", "server listen address")
	_ = flag.Set("logtostderr", "true")
	flag.Parse()
	defer glog.Flush()

	listener, err := net.Listen("tcp", *addr)
	if err != nil {
		log.Fatalf("listen on %s: %v", *addr, err)
	}

	server := grpc.NewServer(grpc.UnaryInterceptor(logUnaryRPC))
	helloworldv1.RegisterGreeterServiceServer(server, &greeterServer{})
	reflection.Register(server)

	log.Printf("gRPC server listening on %s", *addr)
	if err := server.Serve(listener); err != nil {
		log.Fatalf("serve grpc: %v", err)
	}
}
