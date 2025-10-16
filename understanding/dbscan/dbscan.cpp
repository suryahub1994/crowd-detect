#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <cmath>

inline double euclid_distance(const std::vector<double>& a, const std::vector<double>& b) {
    double dx = a[0] - b[0];
    double dy = a[1] - b[1];
    return std::sqrt(dx * dx + dy * dy);
}


void dfs(int el,
         std::unordered_map<int, int>& point_cluster_map,
         int assign_label,
         std::unordered_map<int, bool>& is_visited,
         const std::unordered_set<int>& isCorePoint,
         const std::unordered_map<int, std::set<int>>& neighbor_map)
{
    for (int neighbor : neighbor_map.at(el)) {
        if (!is_visited[neighbor]) {
            is_visited[neighbor] = true;
            point_cluster_map[neighbor] = assign_label;

            if (isCorePoint.count(neighbor)) {
                dfs(neighbor, point_cluster_map, assign_label,
                    is_visited, isCorePoint, neighbor_map);
            }
        }
    }
}

std::unordered_map<int, int> dbscan(const std::vector<std::vector<double>>& points,
                                    double eps, int minPts)
{
    int n = points.size();
    std::unordered_map<int, std::set<int>> neighbor_map;
    std::unordered_map<int, int> neighbor_count;
    std::unordered_set<int> isCorePoint;
    std::unordered_map<int, int> point_cluster_map;
    std::unordered_map<int, bool> is_visited;

    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {  // j starts from i+1
            double d = euclid_distance(points[i], points[j]);
            if (d <= eps) {
                neighbor_map[i].insert(j);
                neighbor_map[j].insert(i);
                neighbor_count[i]++;
                neighbor_count[j]++;
            }
        }
    }

    for (auto& p : neighbor_count) {
        if (p.second >= minPts) {
            isCorePoint.insert(p.first);
        }
    }

    int assign_label = 1;
    for (int i = 0; i < n; ++i) {
        if (isCorePoint.count(i) && !is_visited[i]) {
            is_visited[i] = true;
            point_cluster_map[i] = assign_label;
            dfs(i, point_cluster_map, assign_label,
                is_visited, isCorePoint, neighbor_map);
            assign_label++;
        }
    }

    for (int i = 0; i < n; ++i) {
        if (!is_visited[i]) {
            point_cluster_map[i] = 0; // noise
        }
    }

    return point_cluster_map;
}

int main() {
    std::vector<std::vector<double>> points = {
        {1.0, 1.0}, {1.2, 1.1}, {0.8, 1.0},
        {8.0, 8.0}, {8.2, 8.1}, {100.0, 100.0}
    };

    double eps = 0.5;
    int minPts = 2;

    auto clusters = dbscan(points, eps, minPts);

    std::cout << "DBSCAN Clustering Results:\n";
    for (auto& p : clusters) {
        std::cout << "Point " << p.first << " → Cluster " << p.second << '\n';
    }

    return 0;
}
