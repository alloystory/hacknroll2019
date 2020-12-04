//
//  ViewController.swift
//  Gai Gai
//
//  Created by Stephen Tang on 19/1/19.
//  Copyright © 2019 Stephen Tang. All rights reserved.
//

import UIKit
import Foundation

class ViewController: UIViewController {

    @IBOutlet weak var imageView: UIImageView!
    struct JSONStruct: Codable {
        var data: [JSONInnerStruct]
    }
    
    struct JSONInnerStruct: Codable {
        var name: String
        var description: String
        var category: JSONCategoryStruct
        var provider: String
        var price: String
        var image: String
        var url: String
        var rating: String
    }
    
    struct JSONCategoryStruct: Codable {
        var category_name: String
    }

    var category = 1
    var minPrice = 1
    var maxPrice = 100
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let items = getItems()
        print(items)
        if items.count > 0 {
            imageView.image = items[0].image
            let gesture = UIPanGestureRecognizer(target: self, action: #selector(self.wasDragged(gestureRecognizer:)))
            imageView.isUserInteractionEnabled = true
            imageView.addGestureRecognizer(gesture)
        }
    }
    
    func test() -> String {
        return "hello"
    }
    
    @objc func wasDragged(gestureRecognizer: UIPanGestureRecognizer) {
        let translation = gestureRecognizer.translation(in: view)
        if let image = gestureRecognizer.view {
            image.center = CGPoint(x: self.view.bounds.width / 2 + translation.x, y: self.view.bounds.height / 2 + translation.y)
            let xFromCtr = image.center.x - self.view.bounds.width / 2
            let rotation = CGAffineTransform(rotationAngle: xFromCtr / 1500)
            let scale = min(abs(150 / xFromCtr), 1)
            let opacity = min(abs(100 / xFromCtr), 1)
            let transformation = rotation.scaledBy(x: scale, y: scale)
            image.transform = transformation
            image.alpha = opacity
            
            if gestureRecognizer.state == UIGestureRecognizer.State.ended {
                if image.center.x > 350 {
                    print("yes")
                } else if image.center.x < 0 {
                    print("no")
                }
                
                let rotation = CGAffineTransform(rotationAngle: 0)
                let transformation = rotation.scaledBy(x: 1, y: 1)
                image.transform = transformation
                image.alpha = 1
                image.center = CGPoint(x: self.view.bounds.width / 2, y: self.view.bounds.height - image.bounds.height / 2 - 19)
            }
        }
    }
    
    func getItems() -> [Item] {
        var items: [Item] = []
        let root = "http://178.128.110.173:9000"
        let extn = "/api/items?cat=\(category)&min=\(minPrice)&max=\(maxPrice)"
        let url = URL(string: root + extn)

        let request = URLRequest(url: url! as URL)
        let task = URLSession.shared.dataTask(with: request as URLRequest) { (data, response, error) in
            if error != nil {
                print(error)
            } else {
                if let unwrappedData = data {
                    do {
                        let decoder = JSONDecoder()
                        let results = try decoder.decode(JSONStruct.self, from: unwrappedData)
                        for result in results.data {
                            let imageURL = URL(string: root + result.image)
                            URLSession.shared.dataTask(with: imageURL!, completionHandler: { (imageData, response, error) in
                                if (error != nil) {
                                    print(error)
                                } else {
                                    if let imageData = imageData {
                                        if let outputImage = UIImage(data: imageData) {
                                            let outputPrice = Double(result.price)!
                                            let outputRating = Double(result.rating)!
                                            let outputUrl = URL(string: result.url)!
                                            
                                            let output = Item.init(name: result.name, description: result.description, category_name: result.category.category_name, provider: result.provider, price: outputPrice, image: outputImage, url: outputUrl, rating: outputRating)
                                            items.append(output)
                                        }
                                    }
                                }
                            }).resume()
                        }
                    } catch {
                        print(error)
                    }
                }
            }
        }
        task.resume()
        return items
    }
}
