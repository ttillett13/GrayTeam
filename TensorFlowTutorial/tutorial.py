import tensorflow as tf

# initialize tensor flow nodes
node1 = tf.constant(3.0, dtype=tf.float32)
node2 = tf.constant(4.0) # also tf.float32 implicitly
print("node1:", node1) # will not print the node values
print("node2:", node2)

# make a session and print out the nodes
sess = tf.Session()
print("sess.run(node1, node1):", sess.run([node1, node2])) # will contain the node values

# add node1 and node2 to make node3
node3 = tf.add(node1, node2)
print("node3:", node3)
print("sess.run(node3):", sess.run(node3))

# placeholders that can accept external inputs
a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)

# compound nodes: can apply mathematical operations to nodes to get new nodes
adder_node = a + b  # + provides a shortcut for tf.add(a, b)
print("scalar adder_node:", sess.run(adder_node, {a: 3, b: 4.5}))
print("array adder_node:", sess.run(adder_node, {a: [1, 3], b: [2, 4]}))

add_and_triple = adder_node * 3.
print("add_and_triple:", sess.run(add_and_triple, {a: 3, b: 4.5}))

# Variables: trainable parameters
W = tf.Variable([.3], dtype=tf.float32)
b = tf.Variable([-.3], dtype=tf.float32)
x = tf.placeholder(tf.float32)
linear_model = W * x + b

# must call init to initialze variables
# constants are initialized at creation
init = tf.global_variables_initializer()
sess.run(init)

print("linear model:", sess.run(linear_model, {x: [1, 2, 3, 4]}))

y = tf.placeholder(tf.float32)
squared_deltas = tf.square(linear_model - y)
loss = tf.reduce_sum(squared_deltas)
print("loss:", sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))

# fix the trainable parameters to eliminate loss
fixW = tf.assign(W, [-1.])
fixb = tf.assign(b, [1.])
sess.run([fixW, fixb])
print("fixed loss:", sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))

