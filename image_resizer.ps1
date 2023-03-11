$rating_int = [int]($args[0])
$n = [int]($args[1])
$step = [int]($args[2])
$start = [int](Get-Content -Path ("category_" + $rating_int + "_formatted/category_" + $rating_int + "_formatted_image_count.txt"))

for ($i = 0; $i -lt $n; $i++) {
    .\image_resizer.py $rating_int ($start + $i * $step) ($start + ($i + 1) * $step)
}

$img_cnt = [int](Get-Content -Path ("category_" + $rating_int + "/category_" + $rating_int + "_image_count.txt"))
Write-Output ([System.Math]::Min($img_cnt, $start + $n * $step)) > ("category_" + $rating_int + "_formatted/category_" + $rating_int + "_formatted_image_count.txt")