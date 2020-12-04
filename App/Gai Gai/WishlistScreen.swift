//
//  WishlistScreen.swift
//  Gai Gai
//
//  Created by Stephen Tang on 19/1/19.
//  Copyright © 2019 Stephen Tang. All rights reserved.
//

import UIKit

class WishlistScreen: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    var items: [Item] = []
    var fetchingMore = false

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return items.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let item = items[indexPath.row]
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "wishlistCell") as! WishlistCell
        
        cell.setWishlistCell(item: item)
        
        return cell
    }
    
    func scrollViewDidScroll(_ scrollView: UIScrollView) {
        
        let offsetY = scrollView.contentOffset.y
        let contentHeight = scrollView.contentSize.height
        
        if offsetY > contentHeight - scrollView.frame.height * 4 {
            if !fetchingMore {
                beginBatchFetch()
            }
        }
    }
    
    func beginBatchFetch() {
        fetchingMore = true
        print("fetching more")
//        // TODO
//        let newItems = [16, 17, 18, 19, 20]
//        self.fetchingMore = false
//        self.tableView.reloadData()
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
}
