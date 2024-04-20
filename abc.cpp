#include <iostream>
#include <queue>
#include <vector>
#include <unordered_map>

struct Node {
    int data;
    Node* left;
    Node* right;
};

Node* createNode(int data) {
    Node* newNode = new Node();
    newNode->data = data;
    newNode->left = newNode->right = nullptr;
    return newNode;
}

Node* buildTree(std::vector<int>& nodes, int& index) {
    if (index >= nodes.size() || nodes[index] == -1) {
        return nullptr;
    }

    Node* currentNode = createNode(nodes[index]);
    index++;

    currentNode->left = buildTree(nodes, index);
    currentNode->right = buildTree(nodes, index);

    return currentNode;
}

void printBlastSequence(Node* root, int targetNode) {
    if (!root) {
        return;
    }

    std::queue<Node*> queue;
    queue.push(root);

    std::unordered_map<Node*, Node*> parentMap;
    while (!queue.empty()) {
        Node* currentNode = queue.front();
        queue.pop();

        if (currentNode->left) {
            parentMap[currentNode->left] = currentNode;
            queue.push(currentNode->left);
        }

        if (currentNode->right) {
            parentMap[currentNode->right] = currentNode;
            queue.push(currentNode->right);
        }
    }

    int level = 0;
    Node* target = nullptr;
    queue.push(root);

    while (!queue.empty()) {
        int size = queue.size();

        for (int i = 0; i < size; i++) {
            Node* currentNode = queue.front();
            queue.pop();

            if (currentNode->data == targetNode) {
                target = currentNode;
            }

            if (level > 0) {
                std::cout << currentNode->data << ", ";
            }
        }

        if (level > 0) {
            std::cout << std::endl;
        }

        if (target) {
            if (target->left) {
                queue.push(target->left);
            }

            if (target->right) {
                queue.push(target->right);
            }

            if (parentMap.find(target) != parentMap.end()) {
                queue.push(parentMap[target]);
            }

            target = nullptr;
        }

        level++;
    }
}

int main() {
    int n;
    std::cout << "Enter the number of nodes in the binary tree (including null nodes): ";
    std::cin >> n;

    std::vector<int> nodes(n);
    std::cout << "Enter the nodes in level order (use -1 for null nodes): ";
    for (int i = 0; i < n; i++) {
        std::cin >> nodes[i];
    }

    int index = 0;
    Node* root = buildTree(nodes, index);

    int targetNode;
    std::cout << "Enter the target node: ";
    std::cin >> targetNode;

    std::cout << "Blast sequence:" << std::endl;
    std::cout << targetNode << std::endl;
    printBlastSequence(root, targetNode);

    return 0;
}
