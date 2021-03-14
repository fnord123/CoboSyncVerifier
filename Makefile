SRC = $(wildcard protocol/*.proto)
OBJ = $(patsubst protocol/%.proto, py_protocol/%_pb2.py, $(SRC))

all: $(OBJ)

py_protocol/%_pb2.py: protocol/%.proto
	protoc -I=./protocol --python_out=./py_protocol $<

#all: $(OBJ)
#	protoc -I=./protocol --python_out=. $<

#all: base_pb2.py payload_pb2.py sync_pb2.py transaction_pb2.py

#base_pb2.py:
#	protoc -I=./protocol --python_out=. base.proto

#payload_pb2.py:
#	protoc -I=./protocol --python_out=. payload.proto

#sync_pb2.py:
#	protoc -I=./protocol --python_out=. sync.proto

#transaction_pb2.py:
#	protoc -I=./protocol --python_out=. transaction.proto


