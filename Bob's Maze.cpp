//
// Created by Zhiwei Hu on 5/6/2022.
//
#include <queue>
#include <iostream>
using namespace std;

void matrix_print(vector<vector<int>> matrix){
    for (int i = 0; i<matrix.size(); i++){
        for (int j = 0; j < matrix[0].size(); j++){
            cout<<matrix[i][j]<<",";
        }
        cout<<endl;
    }
}

int bfs(int x, int y, int target_x, int target_y, vector<vector<int>> maze)
{
    // four directions the bob can proceed
    tuple<int,int> up = {0,1};
    tuple<int,int> down = {0,-1};
    tuple<int,int> left = {-1,0};
    tuple<int,int> right = {1,0};

    vector<tuple<int,int>> directions{left,up,right,down};
    int n = maze.size(); // the row number of the maze
    int m = maze[0].size(); // the column number of the maze

    int dis_col_num = m;
    int dis_row_num = n;
    vector<int> dist_row(dis_col_num,-1);
    vector<vector<int>> distance(dis_row_num,dist_row); // same n*m distance matrix with all initial value being -1

    distance[x][y] = 0;
    if ((x==target_x) and (y == target_y))
    {
        return 0;
    }

    queue<tuple<int,int>> q;
    q.push(make_tuple(x,y)); // to put the starting point into the queue
    while (!q.empty()){
        tuple<int,int> curr = q.front();
        int curr_x = get<0>(curr);
        int curr_y = get<1>(curr);
        q.pop(); // after getting the tuple, pop this tuple out of the queue

        for (int i = 0; i<directions.size(); i++)
        {
            int nx = curr_x + get<0>(directions[i]);
            int ny = curr_y + get<1>(directions[i]);
            if ((0<=nx) and (nx<n) and (0<=ny) and (ny<m) and (maze[nx][ny]!=1) and (distance[nx][ny]==-1)){
                distance[nx][ny] = distance[curr_x][curr_y] + 1;
                if ((nx==target_x) and (ny == target_y)){
                    return distance[nx][ny];
                }
                q.push(make_tuple(nx,ny));
            }
        }
    }
    /// might be problem matic here
    return -1;
}

int minMoves(vector<vector<int>> maze, int x, int y){

    // This is the step to find all coins in the maze
    vector<tuple<int,int>> coins;
    for (int i = 0; i<maze.size(); i++){
        for (int k = 0; k<maze[0].size(); k++){
            if (maze[i][k]==2){
                coins.emplace_back(make_tuple(i,k));
            }
        }
    }

    int startX = 0;
    int startY = 0;
    int endX = x;
    int endY = y;

    int num_coins = coins.size();
    if (num_coins==0){
        return bfs(startX,startY,endX,endY,maze); // in this case there's no coin in the maze, simply return the min steps
    }

    int col_num = num_coins+2;
    int row_num = num_coins;
    vector<int> row(col_num,-1);
    vector<vector<int>> coin_dist(row_num,row);

    for (int z = 0; z<num_coins; z++){
        for (int x = 0; x<num_coins; x++){
            coin_dist[z][x] = bfs(get<0>(coins[z]),get<1>(coins[z]),get<0>(coins[x]),get<1>(coins[x]),maze);
        }
        coin_dist[z][num_coins] = bfs(startX,startY,get<0>(coins[z]),get<1>(coins[z]),maze);
        coin_dist[z][num_coins+1] = bfs(get<0>(coins[z]),get<1>(coins[z]),endX,endY,maze);
    }


    for (int k = 0; k<num_coins; k++){
        if ((coin_dist[k][num_coins] == -1) or (coin_dist[k][num_coins+1]==-1)){
            cout<<"This condition is triggered"<<endl;
            return -1;
        }
    }

    // part of dp
    int dp_col = num_coins;
    int dp_row = 1<<num_coins;
    vector<int> dp_row_(dp_col,-1);
    vector<vector<int>> dp(dp_row,dp_row_);


    for (int i = 0; i<num_coins; i++){
        dp[1<<i][i] = coin_dist[i][num_coins];
    }

    for (int mask = 1; mask<(1<<num_coins); mask++){
        for (int i = 0; i<num_coins; i++){
            if ((mask & (1<<i))!=0){
                for (int j = 0; j<num_coins; j++){
                    if ((mask & (1<<j))==0){
                        int next_mask = mask | (1<<j);
                        if ((dp[next_mask][j] == -1) or (dp[next_mask][j]>(dp[mask][i]+coin_dist[i][j]))){
                            dp[next_mask][j] = dp[mask][i] + coin_dist[i][j];
                        }
                    }
                }
            }
        }
    }

    int res = -1;
    int last_mask = (1<<num_coins)-1;
    for (int i = 0; i<num_coins; i++){
        if ((res==-1)||(res>(dp[last_mask][i]+coin_dist[i][num_coins+1]))){
            res = dp[last_mask][i] + coin_dist[i][num_coins+1];
        }
    }
    return res;
}

int main(void)
{
    // a test maze
    vector<vector<int>> maze_1 = {{0,2,0},{1,1,2},{1,0,0}};
    cout<<minMoves(maze_1,2,1)<<endl;
    return 0;
}