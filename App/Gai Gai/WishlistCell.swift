//
//  WishlistCell.swift
//  Gai Gai
//
//  Created by Stephen Tang on 19/1/19.
//  Copyright © 2019 Stephen Tang. All rights reserved.
//

import UIKit

class WishlistCell: UITableViewCell {

    @IBOutlet weak var itemImage: UIImageView!
    @IBOutlet weak var itemName: UILabel!
    @IBOutlet weak var itemProvider: UILabel!
    @IBOutlet weak var itemPrice: UILabel!
    
    func setWishlistCell(item: Item) {
        itemImage.image = item.image
        itemName.text = item.name
        itemProvider.text = item.provider
        itemPrice.text = String(item.price)
    }
}
