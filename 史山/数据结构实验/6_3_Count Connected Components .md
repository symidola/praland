# 6-3 Count Connected Components

#### 题目描述
Write a function to count the number of connected components in a given graph.

### 函数接口定义：
```c
int CountConnectedComponents( LGraph Graph );
```
where LGraph is defined as the following:
```c
typedef struct AdjVNode *PtrToAdjVNode; 
struct AdjVNode{
    Vertex AdjV;
    PtrToAdjVNode Next;
};

typedef struct Vnode{
    PtrToAdjVNode FirstEdge;
} AdjList[MaxVertexNum];

typedef struct GNode *PtrToGNode;
struct GNode{  
    int Nv;
    int Ne;
    AdjList G;
};
typedef PtrToGNode LGraph;
```
The function CountConnectedComponents is supposed to return the number of connected components in the undirected Graph.

### 裁判测试程序样例：
```c
#include <stdio.h>
#include <stdlib.h>

typedef enum {false, true} bool;
#define MaxVertexNum 10  /* maximum number of vertices */
typedef int Vertex;      /* vertices are numbered from 0 to MaxVertexNum-1 */

typedef struct AdjVNode *PtrToAdjVNode; 
struct AdjVNode{
    Vertex AdjV;
    PtrToAdjVNode Next;
};

typedef struct Vnode{
    PtrToAdjVNode FirstEdge;
} AdjList[MaxVertexNum];

typedef struct GNode *PtrToGNode;
struct GNode{  
    int Nv;
    int Ne;
    AdjList G;
};
typedef PtrToGNode LGraph;

LGraph ReadG(); /* details omitted */

int CountConnectedComponents( LGraph Graph );

int main()
{
    LGraph G = ReadG();
    printf("%d\n", CountConnectedComponents(G));

    return 0;
}

/* Your function will be put here */
```
### 输入样例：给定图如下
![示例图片](https://images.ptausercontent.com/82)  
```
8 6
0 7
0 1
2 0
4 1
2 4
3 5
```
#### 输出样例
```
3
```
```
代码长度限制
16 KB
时间限制
400 ms
内存限制
64 MB
```
 
 ### 题解
 ```c
int Visited[10];
void DFS(LGraph Graph, Vertex start){
    if(Visited[start] == 0){
        Visited[start] = 1; 
        PtrToAdjVNode temp = Graph->G[start].FirstEdge;
        while(temp){
            DFS(Graph, temp->AdjV);
            temp = temp->Next;
        }
    }
    return;
}
int CountConnectedComponents( LGraph Graph ){
    int ans = 0;
    for(int i = 0; i < Graph->Nv; i++){
        if(Visited[i] == 0){
            ans++;
            DFS(Graph, i);
        }
    }
    return ans;
}
```
第一次试着传代码哈，刚学完图写的两道基础题。